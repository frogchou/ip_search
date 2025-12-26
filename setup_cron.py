#!/usr/bin/env python3
"""
设置纯真IP数据库每周自动更新的定时任务
"""

import os
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from update_ipdb import update_ipdb
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class IPDBUpdater:
    """IP数据库自动更新器"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
    
    def start(self):
        """启动定时任务"""
        try:
            # 添加每周更新任务
            # 每周一凌晨2点执行更新
            self.scheduler.add_job(
                self._run_update,
                trigger=CronTrigger(day_of_week='1', hour='2', minute='0'),
                id='weekly_ipdb_update',
                name='纯真IP数据库每周自动更新',
                replace_existing=True
            )
            
            # 启动调度器
            self.scheduler.start()
            logger.info("IP数据库自动更新服务已启动，每周一凌晨2点执行更新")
            
            # 显示当前所有任务
            logger.info("当前所有定时任务:")
            for job in self.scheduler.get_jobs():
                logger.info(f"  {job}")
            
            return True
        except Exception as e:
            logger.error(f"启动定时任务失败: {e}")
            return False
    
    def stop(self):
        """停止定时任务"""
        try:
            self.scheduler.shutdown()
            logger.info("IP数据库自动更新服务已停止")
            return True
        except Exception as e:
            logger.error(f"停止定时任务失败: {e}")
            return False
    
    def _run_update(self):
        """执行更新任务"""
        try:
            logger.info("定时更新任务开始执行...")
            update_ipdb()
            logger.info("定时更新任务执行完成")
        except Exception as e:
            logger.error(f"定时更新任务执行失败: {e}")


if __name__ == '__main__':
    updater = IPDBUpdater()
    updater.start()
    
    # 保持程序运行
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        updater.stop()
