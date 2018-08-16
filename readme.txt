1、将python_run.bat文件、hello.py文件和语音的bin文件夹放在同一级目录。
	**注意** ：
		保证语音bin目录下只有从1.bin~16.bin...的bin文件
2、双击python_run.bat
输入：./ + bin文件目录名
回车

生成：voice.bin（集合所有bin的最终可烧写文件） index.txt（所有语音条目的地址索引信息）

3、如果要添加新语音，将新的bin文件修改名称为（数字.bin,按顺序补充在之后）