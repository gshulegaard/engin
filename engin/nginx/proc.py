# -*- coding: utf-8 -*-
# /*
#  * Copyright (C) Nginx, Inc.
#  * All rights reserved.
#  *
#  * Redistribution and use in source and binary forms, with or without
#  * modification, are permitted provided that the following conditions
#  * are met:
#  * 1. Redistributions of source code must retain the above copyright
#  *    notice, this list of conditions and the following disclaimer.
#  * 2. Redistributions in binary form must reproduce the above copyright
#  *    notice, this list of conditions and the following disclaimer in the
#  *    documentation and/or other materials provided with the distribution.
#  *
#  * THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
#  * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#  * ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
#  * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
#  * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#  * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#  * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
#  * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#  * SUCH DAMAGE.
#  */

import hashlib
import re

from dataclasses import dataclass, field
from typing import Any, Dict, List

from coppyr.process import subp

from engin.context import context
from engin.nginx.bin import get_prefix_and_conf_path


@dataclass
class NginxInstanceData:
    pid: int
    version: str
    bin_path: str
    conf_path: str
    prefix: str
    workers: List[Any] = field(default_factory=list)


def launch_method_supported(manager_type: str, ppid: int) -> bool:
    """
    Skip handling if master process is managed by an unsupported launcher
    and/or the launcher is in a container (master process will still show up on host machine's ps output)

    :param manager_type: string - nginx, mysql, or phpfpm, etc.
    :param ppid: int - ppid of master process
    :return:
    """
    launchers = ["supervisord", "supervisorctl", "runsv", "supervise",
                 "mysqld_safe"]

    if ppid not in (0, 1):
        _, out, _ = subp.call(f'ps o "ppid,command" {ppid:d}')
        # take the second line because the first is a header
        launcher_ppid, parent_command = out[1].split(None, 1)

        if not any(x in parent_command for x in launchers):
            context.log.debug(
                f"launching {manager_type} with \"{parent_command}\" is not currently supported"
            )
            return False

        if int(launcher_ppid) not in (0, 1):
            context.log.debug(
                f"master process for {manager_type} is being skipped because its "
                f"launcher ({parent_command}) is in a container"
            )
            return False

    return True


def find() -> List[NginxInstanceData]:
    ps_cmd = "ps xao pid,ppid,command | grep 'nginx[:]'"

    try:
        _, ps_stdout, _ = subp.call(ps_cmd)
    except subp.CoppyrSubpError:
        context.log.debug(f"Failed to find running nginx via '{ps_cmd}'")
        return []

    if not any('nginx: master process' in line for line in ps_stdout):
        context.log.warning(f"No running nginx master processes")
        return []

    master_processes: Dict[int, NginxInstanceData] = {}
    worker_process_cache: Dict[int, List[int]] = {}
    try:
        for line in ps_stdout:
            # parse ps response line:
            # 21355     1 nginx: master process /usr/sbin/nginx
            gwe = re.match(
                r'\s*(?P<pid>\d+)\s+(?P<ppid>\d+)\s+(?P<cmd>.+)\s*', line
            )

            # if we couldn't parse, continue to next line
            if not gwe:
                continue

            pid, ppid, cmd = int(gwe.group('pid')), \
                int(gwe.group('ppid')), \
                gwe.group('cmd').rstrip()

            if "nginx: master process" in cmd:
                if not launch_method_supported("nginx", ppid):
                    continue

                # get path to binary, prefix and conf_path
                try:
                    bin_path, prefix, conf_path, version = get_prefix_and_conf_path(cmd)
                except:
                    context.log.debug('failed to find bin_path, prefix and conf_path for %s' % cmd)
                    context.log.debug('', exc_info=True)
                else:
                    # calculate local id
                    local_string_id = '%s_%s_%s' % (bin_path, conf_path, prefix)
                    local_id = hashlib.sha256(local_string_id.encode('utf-8')).hexdigest()

                    instance = NginxInstanceData(**{
                        'version': version,
                        'bin_path': bin_path,
                        'conf_path': conf_path,
                        'prefix': prefix,
                        'pid': pid,
                        'local_id': local_id
                    })
                    if pid not in master_processes:
                        master_processes[pid] = instance
            # match worker process
            elif 'nginx: worker process' in cmd:
                # because we may parse child processes before the corresponding
                # master is created, just cache the child pids for later adding
                # to the instance data
                worker_process_cache.setdefault(ppid, []).append(pid)

        # now update found instances with child pid data
        for ppid, worker_pids in worker_process_cache.items():
            if ppid in master_processes:
                master_processes[ppid].workers += worker_pids

    except Exception as e:
        exception_name = e.__class__.__name__
        context.log.error('failed to parse ps results due to %s' % exception_name)
        context.log.debug('additional info:', exc_info=True)

    # filter workers with non-executable nginx -V (relative paths, etc)
    results: List[NginxInstanceData] = [
        i for i in master_processes.values()
        if i.bin_path
    ]

    return results
