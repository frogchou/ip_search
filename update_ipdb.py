#!/usr/bin/env python3
"""
纯真IP数据库自动更新脚本
每周自动下载最新的IP数据库并更新本地文件
"""

import os
import requests
import zipfile
import shutil
import logging
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ipdb_update.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 从环境变量获取配置
DOWNLOAD_URL = os.getenv('IPDB_DOWNLOAD_URL')

# 检查下载地址是否配置
if not DOWNLOAD_URL:
    logger.error("未配置IPDB_DOWNLOAD_URL环境变量")
    exit(1)

# 定义路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMP_DIR = os.path.join(BASE_DIR, 'temp')
ZIP_FILE = os.path.join(TEMP_DIR, 'czdb.zip')
CZDBDIR = os.path.join(BASE_DIR, 'czdb')


def update_ipdb():
    """执行IP数据库更新"""
    try:
        logger.info("开始更新IP数据库...")
        
        # 创建临时目录
        os.makedirs(TEMP_DIR, exist_ok=True)
        
        # 下载IP数据库
        logger.info(f"正在下载IP数据库，URL: {DOWNLOAD_URL}")
        response = requests.get(DOWNLOAD_URL, timeout=30)
        response.raise_for_status()
        
        # 保存下载的文件
        with open(ZIP_FILE, 'wb') as f:
            f.write(response.content)
        logger.info(f"成功下载到: {ZIP_FILE}")
        
        # 解压文件
        logger.info("正在解压文件...")
        with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
            # 获取所有文件列表
            file_list = zip_ref.namelist()
            logger.info(f"解压文件列表: {file_list}")
            
            # 提取需要的数据库文件
            for file in file_list:
                if file.endswith('.czdb'):
                    logger.info(f"提取文件: {file}")
                    zip_ref.extract(file, TEMP_DIR)
                    
                    # 复制到czdb目录
                    src_path = os.path.join(TEMP_DIR, file)
                    dst_path = os.path.join(CZDBDIR, os.path.basename(file))
                    shutil.copy2(src_path, dst_path)
                    logger.info(f"已更新: {dst_path}")
        
        # 清理临时文件
        logger.info("清理临时文件...")
        shutil.rmtree(TEMP_DIR)
        os.makedirs(TEMP_DIR, exist_ok=True)  # 重新创建空的临时目录
        
        # 记录更新完成
        logger.info("IP数据库更新完成!")
        
        # 更新版本信息文件
        update_version_info()
        
    except requests.RequestException as e:
        logger.error(f"下载失败: {e}")
        raise
    except zipfile.BadZipFile as e:
        logger.error(f"解压失败: {e}")
        raise
    except Exception as e:
        logger.error(f"更新失败: {e}")
        raise


def update_version_info():
    """更新版本信息文件"""
    version_file = os.path.join(CZDBDIR, 'version.txt')
    try:
        # 获取当前时间作为版本信息
        version_info = {
            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version': f"{datetime.now().strftime('%Y%m%d')}"
        }
        
        with open(version_file, 'w', encoding='utf-8') as f:
            f.write(f"更新时间: {version_info['update_time']}\n")
            f.write(f"版本号: {version_info['version']}\n")
        
        logger.info(f"版本信息已更新: {version_file}")
        return version_info
    except Exception as e:
        logger.error(f"更新版本信息失败: {e}")
        return None


def get_version_info():
    """获取当前版本信息"""
    version_file = os.path.join(CZDBDIR, 'version.txt')
    if not os.path.exists(version_file):
        return {
            'update_time': '未知',
            'version': '未知'
        }
    
    try:
        with open(version_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        version_info = {}
        for line in lines:
            if '更新时间:' in line:
                version_info['update_time'] = line.split('更新时间:')[1].strip()
            elif '版本号:' in line:
                version_info['version'] = line.split('版本号:')[1].strip()
        
        return version_info
    except Exception as e:
        logger.error(f"读取版本信息失败: {e}")
        return {
            'update_time': '未知',
            'version': '未知'
        }


if __name__ == '__main__':
    try:
        update_ipdb()
        version_info = get_version_info()
        logger.info(f"当前数据库版本: {version_info['version']}")
        logger.info(f"最后更新时间: {version_info['update_time']}")
    except Exception as e:
        logger.error(f"更新脚本执行失败: {e}")
        exit(1)