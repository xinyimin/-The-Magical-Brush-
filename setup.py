from setuptools import setup, find_packages

# 读取 requirements.txt 文件内容
with open('requirements.txt') as f:
    required = f.read().splitlines()
    
setup(
    name='The Magical Brush',  # 包名
    version='0.1',  # 版本号
    packages=find_packages(),  # 自动查找项目中的包
    install_requires= required,
    entry_points={
        'console_scripts': [
            # 可以定义命令行工具的入口点
            # 例如: 'your_script = your_package.module:main_function'
        ],
    },
    # 其他可选参数
    author='suiying',
    author_email='656740015@qq.com',
    description='A short description of your project',
    long_description=open('README.md').read(),
    long_description_content_type='',  # 如果使用markdown作为README文件
    url='',
    classifiers=[
        # 分类信息，用于PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10.6',  # 对Python版本的要求
)