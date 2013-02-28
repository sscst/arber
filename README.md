微博备份小工具
=============  
依赖：MySQLdb  
1. 打开config.json文件配置token,mysql信息
2. 运行linkDB.py  
  *cd arber*  
  *python linkDB.py*  
3. 然后退出arber文件目录，运行之  
		*cd ..*  
		*python arber*  
4. 基本功能介绍：  
     working:查询正在工作的列表（输入working即可）  
     finish:查询完成的列表  （输入finish即可）  
     a 后跟昵称 备份某人微博  
	eg. a 一找小七  
     down 后跟昵称 将某人微博（前提是已经完成了备份）导成TXT文件，后跟 top 数字 可以获得最热门的N个微博  
	eg. down 一找小七 top 50     ----->(获取这个微博帐号最热门的50条)
5. 如果因为各种原因导致程序停止，不用担心，再次重新启动程序即可，不会影响效果  



	
    
