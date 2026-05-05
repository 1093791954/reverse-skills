# UE Reverse Series Notes

Total articles: 27

## 1. 1.UE-准备环境（一）-账号注册和打开虚幻引擎源码页面

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151894343
- Description: æç« æµè§éè¯»984æ¬¡ï¼ç¹èµ4æ¬¡ï¼æ¶è10æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ èå¹»å¼æ UnrealEngine_ç¨ueå¼åæ¸¸æéè¦æ³¨åè´¦å·å?

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
内容参考于：微尘网络安全 
UE，全称UnrealEditor，中文名虚幻，它是现代比较火的游戏引擎，很多游戏都使用了它，它是开源的 
 
 UE官网：www.unrealengine.com/zh-CN/ 
 
 
这里只会写逆向时需要的技术，学习完无法成为合格的游戏开发，虚幻引擎它会提供很多接口很多函数，也就是说虚幻引擎有很多写好的东西（库）给我们使用，然后虚幻引擎的是开源的，也就能看到一些源代码，然后就可以通过分析虚幻引擎的源码，去找清楚它的偏移有多少层、找清楚函数地址。 
从GitHub中下载虚幻引擎源码： 
这是虚幻引擎源码下载地址：https://github.com/EpicGames/UnrealEngine 
直接打开是下图的样子，无法访问，需要进行一些操作才可以打开 
 
下方的操作很最重要，关系到是否可以打开虚幻引擎源码页面 
 
 想下载虚幻引擎源码，它是需要有一个GitHub账号，进入GitHub页面（https://github.com/）点击下图红框，下方是注册GitHub账号，如果已有账号可以忽略，直接去下方看UE账号注册 
  
 然后如下图输入相关内容 
  
 点击下图红框进行人机验证 
  
 人机验证 
  
 然后人机验证通过给邮箱发送激活验证码 
  
 输入邮箱里的验证码 
  
 下图红框就是验证码的邮件 
  
 注册完成，然后输入刚注册时使用的邮箱和密码，然后点击Sign in登录 
 
 
注册UE账号，下方是注册UE账号如果有直接登录，登录后跳过这里的UE注册直接去下方的UE和GitHub账号关联 
 
 然后进入UE官网注册账号，首先点击下图红框的登录 
  
 然后点击创建账户 
  
 然后选择否 
  
 随便输入一个成年后的年月日，然后点击继续 
  
 输入一个邮箱 
  
 然后 
  
 然后登录邮箱查看验证码 
  
 下图红框的就是验证码邮件，输入之后点击上图的继续就注册完成了，然后登录 
  
  
  
 
关联GitHub，这一步很重要，没有它就没办法看到虚幻引擎源码 
 
 登录之后，根据下图红框进行操作 
  
 然后选择已关联账户，然后找到GitHub点击关联，注意 已关联账户 这几个字在未来可能会变成别的字，不管变成什么它肯定有下图的一个关联账号的页面，去找这个页面就可以了 
  
 点击关联后，勾选下图红框 
  
 然后把下图红框的滚动条拉到底 
  
 然后点击我同意 
  
 然后点击关联账户 
  
 如果当前浏览器已经登录了GitHub，就会直接弹出下图红框的页面，否则弹出下图红框页面的内容是登录GitHub账号，登录完再是下图红框的页面 
  
 然后点击下图红框进行关联 
  
 然后点击关联完成 
  
 然后如下图关联成功 
  
  
 
然后打开注册GitHub时用到的邮箱，会有下图的邮件，点击 Join@EpicGames 
 
中文翻译 
 
点击完上图的按钮后，会跳转到下图的页面，然后点击Join Epic Games 
 
中文翻译 
 
然后就加入了虚幻引擎 
 
中文翻译 
 
如下图源码页面也就能在正常打开了

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
内容参考于：微尘网络安全 
UE，全称UnrealEditor，中文名虚幻，它是现代比较火的游戏引擎，很多游戏都使用了它，它是开源的 
 
 UE官网：www.unrealengine.com/zh-CN/ 
 
 
这里只会写逆向时需要的技术，学习完无法成为合格的游戏开发，虚幻引擎它会提供很多接口很多函数，也就是说虚幻引擎有很多写好的东西（库）给我们使用，然后虚幻引擎的是开源的，也就能看到一些源代码，然后就可以通过分析虚幻引擎的源码，去找清楚它的偏移有多少层、找清楚函数地址。 
从GitHub中下载虚幻引擎源码： 
这是虚幻引擎源码下载地址：https://github.com/EpicGames/UnrealEngine 
直接打开是下图的样子，无法访问，需要进行一些操作才可以打开 
 
下方的操作很最重要，关系到是否可以打开虚幻引擎源码页面 
 
 想下载虚幻引擎源码，它是需要有一个GitHub账号，进入GitHub页面（https://github.com/）点击下图红框，下方是注册GitHub账号，如果已有账号可以忽略，直接去下方看UE账号注册 
  
 然后如下图输入相关内容 
  
 点击下图红框进行人机验证 
  
 人机验证 
  
 然后人机验证通过给邮箱发送激活验证码 
  
 输入邮箱里的验证码 
  
 下图红框就是验证码的邮件 
  
 注册完成，然后输入刚注册时使用的邮箱和密码，然后点击Sign in登录 
 
 
注册UE账号，下方是注册UE账号如果有直接登录，登录后跳过这里的UE注册直接去下方的UE和GitHub账号关联 
 
 然后进入UE官网注册账号，首先点击下图红框的登录 
  
 然后点击创建账户 
  
 然后选择否 
  
 随便输入一个成年后的年月日，然后点击继续 
  
 输入一个邮箱 
  
 然后 
  
 然后登录邮箱查看验证码 
  
 下图红框的就是验证码邮件，输入之后点击上图的继续就注册完成了，然后登录 
  
  
  
 
关联GitHub，这一步很重要，没有它就没办法看到虚幻引擎源码 
 
 登录之后，根据下图红框进行操作 
  
 然后选择已关联账户，然后找到GitHub点击关联，注意 已关联账户 这几个字在未来可能会变成别的字，不管变成什么它肯定有下图的一个关联账号的页面，去找这个页面就可以了 
  
 点击关联后，勾选下图红框 
  
 然后把下图红框的滚动条拉到底 
  
 然后点击我同意 
  
 然后点击关联账户 
  
 如果当前浏览器已经登录了GitHub，就会直接弹出下图红框的页面，否则弹出下图红框页面的内容是登录GitHub账号，登录完再是下图红框的页面 
  
 然后点击下图红框进行关联 
  
 然后点击关联完成 
  
 然后如下图关联成功 
  
  
 
然后打开注册GitHub时用到的邮箱，会有下图的邮件，点击 Join@EpicGames 
 
中文翻译 
 
点击完上图的按钮后，会跳转到下图的页面，然后点击Join Epic Games 
 
中文翻译 
 
然后就加入了虚幻引擎 
 
中文翻译 
 
如下图源码页面也就能在正常打开了

## 2. 2.UE-准备环境（二）-下载虚幻引擎源码和搞成vs项目并使用vs打开

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151924469
- Description: æç« æµè§éè¯»1.5kæ¬¡ï¼ç¹èµ25æ¬¡ï¼æ¶è7æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ UE èå¹» èå¹»å¼æ UnrealEngine_commit.gitdeps.xml ä¸è½½

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：1.UE-准备环境（一）-账号注册和打开虚幻引擎源码页面 
需要翻墙才可以访问，不会翻墙的东西已经放到百度网盘了，去百度网盘里找 
UE的源码很大，要准备好内存空间，它有近40G大小 
 
打开虚幻引擎代码的GitHub(https://github.com/EpicGames/UnrealEngine)，如下图 
 
点击下图蓝框，可以出现下图红框的内容，这是虚幻引擎的版本，有ue5、ue4，下载什么版本取决于要搞的游戏 
 
查看游戏使用的ue版本，如下图红框ue的游戏，文件名都会有Shipping 
 
然后右击选择属性 
 
然后打开详细信息标签，如下图红框的文件版本，这就是ue的版本，它使用的是4.257.0 
 
然后来到ue的GitHub找到4.27.2，如下图红框Tab页签下的版本内容比Branches页签下的全 
 
然后如下图红框下载源码 
 
如下图红框下载完解压 
 
然后如下图进入ue的文件夹，现在的文件是不全的 
 
然后双击运行下图红框文件 
 
双击运行后，会出现403错误，这是因为UE的服务器迁移，我们下载的源码中的配置文件服务器地址没有跟着变导致的，这里需要手动修改一下 
 
上图的原因，如下图官网解释和解决，下图是搜索 UnrealEngine-4.27.2-release Setup.bat 403 这个关键字得到的 
 
中文翻译 
 
然后点击下图红框文件 
 
然后找到对应的版本4.27.2，然后点击下图红框的Commit.gitdeps.xml文件进行下载 
 
下载完成后，如下图把刚下载的Commit.gitdeps.xml文件拖到箭头所示的目录里，也就是把源码中原本的Commit.gitdeps.xml文件替换成从上图中下载的文件 
 
然后再次运行Setup.bat 
 
如下图它就可以下载了，它很大耐心等待 
 
下载完成 
 
然后它可能会弹出下图的弹框，中文意思是把UnrealEngine注册成文件类型，这里选的是 
 
然后可能会弹出下图的弹框，选择下图红框进行下载和安装，如果下图没办法安装，可以使用搜索引擎搜索.NET Framework3.5下载，找一找资料 
 
点击上图红框后下载中 
 
不需要等上图安装完，只要等Setup.bat下载完，就可以运行下图红框的文件，它会把项目搞成vs项目 
 
然后它也会出错，它找不到.NET Framework 4.6.2组件 
 
安装.NET Framework 4.6.2组件，运行 VisualStudioSetup-2022-Community 这个程序，也就是vs2022安装程序，点击下图红框的修改 
 
如下图红框在单个组件中，找到.NET Framework 4.6.2勾选SDK和目标包 
 
勾选完点击修改 
 
点击修改后出现下图的弹框，说明vs2022正在运行，需要把它关了，然后点重试 
 
等待下载完成 
 
上图下载完成和安装完成后再次运行下图红框的文件 
 
如下图等待完成 
 
完成后就是vs可以认识的项目了，如下图红框 
 
双击下图红框文件，它会使用vs进行打开，如果电脑上有多个vs版本，它会使用.sln文件默认 
 
默认程序设置如下图 
 
然后更新到4.8，下图的提示会弹出多次，都选更新到4.8，也就是都根据下图红框进行选择和操作 
 
然后常看的源码在下图红框的目录里

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：1.UE-准备环境（一）-账号注册和打开虚幻引擎源码页面 
需要翻墙才可以访问，不会翻墙的东西已经放到百度网盘了，去百度网盘里找 
UE的源码很大，要准备好内存空间，它有近40G大小 
 
打开虚幻引擎代码的GitHub(https://github.com/EpicGames/UnrealEngine)，如下图 
 
点击下图蓝框，可以出现下图红框的内容，这是虚幻引擎的版本，有ue5、ue4，下载什么版本取决于要搞的游戏 
 
查看游戏使用的ue版本，如下图红框ue的游戏，文件名都会有Shipping 
 
然后右击选择属性 
 
然后打开详细信息标签，如下图红框的文件版本，这就是ue的版本，它使用的是4.257.0 
 
然后来到ue的GitHub找到4.27.2，如下图红框Tab页签下的版本内容比Branches页签下的全 
 
然后如下图红框下载源码 
 
如下图红框下载完解压 
 
然后如下图进入ue的文件夹，现在的文件是不全的 
 
然后双击运行下图红框文件 
 
双击运行后，会出现403错误，这是因为UE的服务器迁移，我们下载的源码中的配置文件服务器地址没有跟着变导致的，这里需要手动修改一下 
 
上图的原因，如下图官网解释和解决，下图是搜索 UnrealEngine-4.27.2-release Setup.bat 403 这个关键字得到的 
 
中文翻译 
 
然后点击下图红框文件 
 
然后找到对应的版本4.27.2，然后点击下图红框的Commit.gitdeps.xml文件进行下载 
 
下载完成后，如下图把刚下载的Commit.gitdeps.xml文件拖到箭头所示的目录里，也就是把源码中原本的Commit.gitdeps.xml文件替换成从上图中下载的文件 
 
然后再次运行Setup.bat 
 
如下图它就可以下载了，它很大耐心等待 
 
下载完成 
 
然后它可能会弹出下图的弹框，中文意思是把UnrealEngine注册成文件类型，这里选的是 
 
然后可能会弹出下图的弹框，选择下图红框进行下载和安装，如果下图没办法安装，可以使用搜索引擎搜索.NET Framework3.5下载，找一找资料 
 
点击上图红框后下载中 
 
不需要等上图安装完，只要等Setup.bat下载完，就可以运行下图红框的文件，它会把项目搞成vs项目 
 
然后它也会出错，它找不到.NET Framework 4.6.2组件 
 
安装.NET Framework 4.6.2组件，运行 VisualStudioSetup-2022-Community 这个程序，也就是vs2022安装程序，点击下图红框的修改 
 
如下图红框在单个组件中，找到.NET Framework 4.6.2勾选SDK和目标包 
 
勾选完点击修改 
 
点击修改后出现下图的弹框，说明vs2022正在运行，需要把它关了，然后点重试 
 
等待下载完成 
 
上图下载完成和安装完成后再次运行下图红框的文件 
 
如下图等待完成 
 
完成后就是vs可以认识的项目了，如下图红框 
 
双击下图红框文件，它会使用vs进行打开，如果电脑上有多个vs版本，它会使用.sln文件默认 
 
默认程序设置如下图 
 
然后更新到4.8，下图的提示会弹出多次，都选更新到4.8，也就是都根据下图红框进行选择和操作 
 
然后常看的源码在下图红框的目录里

## 3. 3.UE-探索GetName的加密算法（一）-GName（FName和UObjectBase结构）

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151971727
- Description: æç« æµè§éè¯»1.2kæ¬¡ï¼ç¹èµ11æ¬¡ï¼æ¶è14æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ UE UnrealEngine_ue4å¯»æ¾gname

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：2.UE-准备环境（二）-下载虚幻引擎源码和搞成vs项目并使用vs打开 
GName它是，首先游戏它有一个id，这个id的内容比如是110010（有比它长的也有比它短的）可以理解为它就是一串数字，这个数字它会起到一个引导作用，然后在GName的的内存里它有多级指针（就是内存里的值放的是内存地址，然后这个内存地址里的值放的还是内存地址，这就是多级指针），然后它会使用id的一部分去找某个内存地址里的值，比如110010，它用11去找GName+11位置的值，这个值是个内存地址比如0x1000，找到这个内存地址之后再用00值，去0x1000+0位置去找值，找的值后它还是个内存地址，比如0x2000，然后用10去0x2000+10位置去找，然后就得到一个数据（文字），这就是GName，ue里的字符串（文字）都是用GName这种方式进行的加密，它所有的字符串都要通过一个id来得到，这里看不懂没关系会用会复制就行，会用之后就可以看懂了 
然后GName的获取是通过GetName函数来得到的，然后接下来就去ue源码中搜索GetName，如下图搜索的时候最后要加一个(括号 
 
然后点击全部显示，这个内容它有很多，电脑性能不高可能要搜索很久 
 
搜索完之后找Source-》Runtime-》Engine里面的，它里面的GName都可以（有些按着CTRL鼠标点击没办法跳转，要找一个可以跳转的） 
 
下图红框的GName可以按着CTRL鼠标点击GName进行跳转 
 
按着CTRL鼠标左键单击下图红框 
 
然后就会跳转到下图红框位置，它在UObjectBaseUtility.h文件里 
 
要了解的FString，也就是下图红框的类型（结构），然后按着CTRL鼠标左键单击下图红框位置 
 
然后就进入了FString结构，它是一个类，也就是说GetName()函数它返回了一个FString类 
 
FString结构它里面有很多东西，只需要了解DataType，如下图红框，DataType是一个TArray<TCHAR>结构，这里不需要理解TArray<TCHAR>这个写法（不要浪废时间去了解这个东西，后面慢慢就会懂，就算不懂会复制代码也能玩，只需要指定它能达到一个什么效果就可以了），然后FString结构里只有一个Data成员变量 
 
然后TCHAR的类型FPlatformTypes::TCHAR 
 
然后FPlatformTypes::TCHAR的类型WIDECHAR 
 
然后WIDECHAR的类型wchar_t，也就是说TArray<TCHAR>实际上是TArray<wchar_t>这样的 
 
然后如下图红框 TArray 是一个类 
 
TArray 它里面也有很多东西，挨个看会很乱，需要了解的是 TArray 是一个类，它里面有三个成员

```text
class TArray{
    T* data;// 这个T*是TArray<TCHAR>里的TCHAR，也就是TCHAR*
    int num;// data的内存空间里面用了多少
    int maxNum;// data的内存空间最大，也就是它表示了data的内存空间有多大
}
// 这个TArray会经常用到

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：2.UE-准备环境（二）-下载虚幻引擎源码和搞成vs项目并使用vs打开 
GName它是，首先游戏它有一个id，这个id的内容比如是110010（有比它长的也有比它短的）可以理解为它就是一串数字，这个数字它会起到一个引导作用，然后在GName的的内存里它有多级指针（就是内存里的值放的是内存地址，然后这个内存地址里的值放的还是内存地址，这就是多级指针），然后它会使用id的一部分去找某个内存地址里的值，比如110010，它用11去找GName+11位置的值，这个值是个内存地址比如0x1000，找到这个内存地址之后再用00值，去0x1000+0位置去找值，找的值后它还是个内存地址，比如0x2000，然后用10去0x2000+10位置去找，然后就得到一个数据（文字），这就是GName，ue里的字符串（文字）都是用GName这种方式进行的加密，它所有的字符串都要通过一个id来得到，这里看不懂没关系会用会复制就行，会用之后就可以看懂了 
然后GName的获取是通过GetName函数来得到的，然后接下来就去ue源码中搜索GetName，如下图搜索的时候最后要加一个(括号 
 
然后点击全部显示，这个内容它有很多，电脑性能不高可能要搜索很久 
 
搜索完之后找Source-》Runtime-》Engine里面的，它里面的GName都可以（有些按着CTRL鼠标点击没办法跳转，要找一个可以跳转的） 
 
下图红框的GName可以按着CTRL鼠标点击GName进行跳转 
 
按着CTRL鼠标左键单击下图红框 
 
然后就会跳转到下图红框位置，它在UObjectBaseUtility.h文件里 
 
要了解的FString，也就是下图红框的类型（结构），然后按着CTRL鼠标左键单击下图红框位置 
 
然后就进入了FString结构，它是一个类，也就是说GetName()函数它返回了一个FString类 
 
FString结构它里面有很多东西，只需要了解DataType，如下图红框，DataType是一个TArray<TCHAR>结构，这里不需要理解TArray<TCHAR>这个写法（不要浪废时间去了解这个东西，后面慢慢就会懂，就算不懂会复制代码也能玩，只需要指定它能达到一个什么效果就可以了），然后FString结构里只有一个Data成员变量 
 
然后TCHAR的类型FPlatformTypes::TCHAR 
 
然后FPlatformTypes::TCHAR的类型WIDECHAR 
 
然后WIDECHAR的类型wchar_t，也就是说TArray<TCHAR>实际上是TArray<wchar_t>这样的 
 
然后如下图红框 TArray 是一个类 
 
TArray 它里面也有很多东西，挨个看会很乱，需要了解的是 TArray 是一个类，它里面有三个成员 

```text
class TArray{
    T* data;// 这个T*是TArray<TCHAR>里的TCHAR，也就是TCHAR*
    int num;// data的内存空间里面用了多少
    int maxNum;// data的内存空间最大，也就是它表示了data的内存空间有多大
}
// 这个TArray会经常用到

```
 
然后也就是说GetName函数它返回了一个TArray<TCHAR>类型的Data，到这就是FString类型的说明 
然后还有一个GetFName，如下图红框GetFName返回值是NamePrivate 
 
NamePrivate的类型，如下图红框是一个FName类型 
 
然后NamePrivate它在UObjectBase类里 
 
然后NamePrivate在UObjectBase类里的第4个成员函数为位置 
 
然后EObjectFlags，它是一个枚举（枚举就是一个固定值的集合）类型，4字节，如下图每个值是8位数，两个数字表示1字节，一共是4字节 
 
然后UObjectBase类里存在虚函数，所以如果得到了一个UObjectBase类型就可以通过读取它8（虚函数的内存地址）+4（ObjectFlags的值，它是一个枚举（枚举就是一个固定值的集合）类型，4字节）*4（InternalIndex的值）+8（ClassPrivate的值，UClass*是一个指针，指针是8字节）字节的位置（8+4+4+8）来得到NamePrivate， 
 
8+4+4+8的结果是24，24的十六进制是18 
 
UObjectBase说明 

```text
// ###########################################################################
// 重要警告：内存偏移为【默认编译配置（MSVC、UE 4.x/5.x、无特殊优化）下的理论值】
// 1. 受环境影响（32/64位、编译器版本、UE版本、内存对齐），实际需用ReClass/IDA验证
// 2. 不可硬编码依赖偏移值！UE更新或编译配置变化会导致偏移失效
// 3. 核心前提：含虚函数的类（UObjectBase有虚析构）首地址会自动添加【虚函数表指针（vtable ptr）】
//    - 32位：vtable ptr占4字节（0x4）；64位：vtable ptr占8字节（0x8）
//    - 所有成员偏移均以vtable ptr为基准起点计算
// 4. UE类型约定：EObjectFlags（枚举）=int32(4字节)、FName=8字节(2个int32)、指针=4/8字节（32/64位）
// ###########################################################################

// UObjectBase：Unreal Engine所有对象的基类，提供统一的对象基础属性与生命周期管理
class COREUOBJECT_API UObjectBase
{
	// 友元声明：允许指定类/函数访问私有成员（内部管理需求，不影响内存偏移）
	friend class UObjectBaseUtility;
	friend struct Z_Construct_UClass_UObject_Statics;
	friend class FUObjectArray; // 需访问InternalIndex定位对象
	friend class FUObjectAllocator; // 需访问析构函数管理内存
	friend COREUOBJECT_API void UObjectForceRegistration(UObjectBase* Object, bool bCheckForModuleRelease);
	friend COREUOBJECT_API void InitializePrivateStaticClass(
		class UClass* TClass_Super_StaticClass,
		class UClass* TClass_PrivateStaticClass,
		class UClass* TClass_WithinClass_StaticClass,
		const TCHAR* PackageName,
		const TCHAR* Name
		);

protected:
	// 空构造函数：子类继承占位，不影响内存布局
	UObjectBase() : NamePrivate(NoInit) {}
	// 引导启动构造函数：初始化对象标志，不影响内存布局
	UObjectBase(EObjectFlags InFlags);
public:
	// 静态分配构造函数：常规对象创建用，不影响内存布局
	UObjectBase(UClass* InClass, EObjectFlags InFlags, EInternalObjectFlags InInternalFlags, UObject* InOuter, FName InName);
	// 虚析构函数：触发添加vtable ptr（类首地址隐藏成员），是内存偏移的基准起点
	virtual ~UObjectBase();

	// 静态函数：GC引用标记，不占用实例内存（无偏移）
	static void EmitBaseReferences(UClass* RootClass);

protected:
	// 底层重命名函数：不占用实例内存（无偏移）
	void LowLevelRename(FName NewName, UObject* NewOuter = NULL);
	// 虚函数：注册依赖，不占用实例内存（无偏移）
	virtual void RegisterDependencies() {}
	// 注册函数：不占用实例内存（无偏移）
	void Register(const TCHAR* PackageName, const TCHAR* Name);
	// 虚函数：延迟注册，不占用实例内存（无偏移）
	virtual void DeferredRegister(UClass* UClassStaticClass, const TCHAR* PackageName, const TCHAR* Name);

private:
	// 添加对象函数：不占用实例内存（无偏移）
	void AddObject(FName Name, EInternalObjectFlags InSetInternalFlags);

public:
	// 有效性检查函数：不占用实例内存（无偏移）
	bool IsValidLowLevel() const;
	// 快速有效性检查函数：不占用实例内存（无偏移）
	bool IsValidLowLevelFast(bool bRecursive = true) const;

	// 内联函数：获取UniqueID，不占用实例内存（无偏移）
	FORCEINLINE uint32 GetUniqueID() const { return (uint32)InternalIndex; }
	// 内联函数：获取类模板，不占用实例内存（无偏移）
	FORCEINLINE UClass* GetClass() const { return ClassPrivate; }
	// 内联函数：获取所有者，不占用实例内存（无偏移）
	FORCEINLINE UObject* GetOuter() const { return OuterPrivate; }
	// 内联函数：获取名字，不占用实例内存（无偏移）
	FORCEINLINE FName GetFName() const { return NamePrivate; }

	// 静态函数：移除类名前缀，不占用实例内存（无偏移）
	static FString RemoveClassPrefix(const TCHAR* ClassName);
	// 获取外部包函数：不占用实例内存（无偏移）
	UPackage* GetExternalPackage() const;
	// 设置外部包函数：不占用实例内存（无偏移）
	void SetExternalPackage(UPackage* InPackage);
	// 内部获取外部包函数：不占用实例内存（无偏移）
	UPackage* GetExternalPackageInternal() const;

protected:
	// 内联函数：设置对象标志，不占用实例内存（无偏移）
	FORCEINLINE void SetFlagsTo(EObjectFlags NewFlags) {
		checkfSlow((NewFlags & ~RF_AllFlags) == 0, TEXT("%s flagged as 0x%x but is trying to set flags to RF_AllFlags"), *GetFName().ToString(), (int)ObjectFlags);
		ObjectFlags = NewFlags;
	}

public:
	// 内联函数：获取对象标志，不占用实例内存（无偏移）
	FORCEINLINE EObjectFlags GetFlags() const {
		checkfSlow((ObjectFlags & ~RF_AllFlags) == 0, TEXT("%s flagged as RF_AllFlags"), *GetFName().ToString());
		return ObjectFlags;
	}

	// 原子设置标志函数：不占用实例内存（无偏移）
	FORCENOINLINE void AtomicallySetFlags(EObjectFlags FlagsToAdd) {
		int32 OldFlags = 0;
		int32 NewFlags = 0;
		do {
			OldFlags = ObjectFlags;
			NewFlags = OldFlags | FlagsToAdd;
		} while (FPlatformAtomics::InterlockedCompareExchange((int32*)&ObjectFlags, NewFlags, OldFlags) != OldFlags);
	}

	// 原子清除标志函数：不占用实例内存（无偏移）
	FORCENOINLINE void AtomicallyClearFlags(EObjectFlags FlagsToClear) {
		int32 OldFlags = 0;
		int32 NewFlags = 0;
		do {
			OldFlags = ObjectFlags;
			NewFlags = OldFlags & ~FlagsToClear;
		} while (FPlatformAtomics::InterlockedCompareExchange((int32*)&ObjectFlags, NewFlags, OldFlags) != OldFlags);
	}

private:
	// ###########################################################################
	// 以下为【实例成员】：按声明顺序布局，偏移基于vtable ptr计算
	// ###########################################################################

	/**
	 * 对象标志：存储对象公开状态（如可编辑、需GC）
	 * 类型：EObjectFlags（枚举，UE默认按int32存储，4字节）
	 * 32位偏移：0x4 → 原因：vtable ptr占0x4（0x0-0x3），紧跟其后从0x4开始
	 * 64位偏移：0x8 → 原因：vtable ptr占0x8（0x0-0x7），紧跟其后从0x8开始
	 * 对齐：int32按4字节对齐，与前序vtable ptr（4/8字节）自然对齐，无间隙
	 */
	EObjectFlags					ObjectFlags;

	/**
	 * 全局对象数组索引：对象在GObjectArray中的位置（仅存活时唯一）
	 * 类型：int32（4字节）
	 * 32位偏移：0x8 → 原因：前序ObjectFlags占0x4（0x4-0x7），0x4+0x4=0x8
	 * 64位偏移：0xC → 原因：前序ObjectFlags占0x4（0x8-0xB），0x8+0x4=0xC
	 * 对齐：int32按4字节对齐，64位下0xC是4的倍数，无间隙
	 */
	int32							InternalIndex;

	/**
	 * 对象类模板：指向对象所属的UClass（如ACharacter、UBlueprint）
	 * 类型：UClass*（指针，32位4字节，64位8字节）
	 * 32位偏移：0xC → 原因：前序InternalIndex占0x4（0x8-0xB），0x8+0x4=0xC
	 * 64位偏移：0x10 → 原因：前序InternalIndex占0x4（0xC-0xF），但64位指针需8字节对齐，0xF+1=0x10（补4字节间隙）
	 * 对齐：64位下指针按8字节对齐，0x10是8的倍数，满足对齐要求
	 */
	UClass*							ClassPrivate;

	/**
	 * 对象名字：存储对象的FName（高效字符串，固定8字节）
	 * 类型：FName（含2个int32成员：Index和Number，共8字节）
	 * 32位偏移：0x10 → 原因：前序ClassPrivate占0x4（0xC-0xF），0xC+0x4=0x10
	 * 64位偏移：0x18 → 原因：前序ClassPrivate占0x8（0x10-0x17），0x10+0x8=0x18
	 * 对齐：FName按4字节对齐（内部int32成员），32/64位下均无间隙
	 */
	FName							NamePrivate;

	/**
	 * 对象所有者：指向对象的Outer（上级对象，构成层级关系）
	 * 类型：UObject*（指针，32位4字节，64位8字节）
	 * 32位偏移：0x18 → 原因：前序NamePrivate占0x8（0x10-0x17），0x10+0x8=0x18
	 * 64位偏移：0x20 → 原因：前序NamePrivate占0x8（0x18-0x1F），0x18+0x8=0x20
	 * 对齐：指针按自身大小对齐，32/64位下均无间隙
	 */
	UObject*						OuterPrivate;
	
	// 友元声明：蓝图重实例化、上下文管理用，不影响内存布局
	friend class FBlueprintCompileReinstancer;
	friend class FContextObjectManager;

	// 私有函数：设置类模板，不占用实例内存（无偏移）
	void SetClass(UClass* NewClass);

#if HACK_HEADER_GENERATOR
	// UHT序列化用，不影响内存布局
	friend struct FObjectBaseArchiveProxy;
#endif // HACK_HEADER_GENERATOR
};

```
 
FString 

```text
// ###########################################################################
// FString 内存偏移核心前提：
// 1. FString 无虚函数（无隐藏虚表指针），内存布局仅包含唯一成员 `Data`（TArray<TCHAR>）
// 2. 偏移完全依赖 `TArray<TCHAR>` 的内存结构（UE 4.x/5.x 通用，32/64位差异主要来自指针大小和对齐）
// 3. TArray 核心结构（固定）：`DataPtr`（存储字符数据的指针）、`Num`（当前元素数，含null终止符）、`Capacity`（已分配容量）
// ###########################################################################

// FString：Unreal Engine 动态字符串类，基于 TArray<TCHAR> 实现，自动管理内存和字符编码
class CORE_API FString
{
private:
	friend struct TContainerTraits<FString>;

	/** 
	 * 核心存储成员：TArray<TCHAR> 类型，存储字符串数据（含末尾的 null 终止符）
	 * 内存偏移说明（关键！）：
	 * - 32位环境：偏移 0x0（FString 无虚表，第一个成员从实例首地址开始）
	 * - 64位环境：偏移 0x0（同上，无虚表，无成员前填充）
	 * 为什么偏移是 0x0？
	 * FString 仅含这一个非静态成员，且无虚函数（无隐藏虚表指针），成员布局从实例首地址（0x0）开始，无任何偏移
	 * 
	 * 补充：TArray<TCHAR> 内部结构的偏移（决定 FString 整体内存占用）
	 * TArray 是 FString 的“数据载体”，其内部三成员的偏移如下：
	 */
	typedef TArray<TCHAR> DataType;
	DataType Data;  // 32位/64位偏移均为 0x0，FString 实例首地址 = Data 首地址

	// -------------------------- TArray<TCHAR> 内部成员偏移（基于 FString::Data 偏移 0x0 推导） --------------------------
	// TArray 结构：[DataPtr（字符数据指针）] → [Num（元素数）] → [Capacity（容量）]
	// 1. 32位环境（指针占 4 字节，int32 占 4 字节，无对齐填充）：
	//    - DataPtr（TCHAR*）：偏移 0x0（相对于 Data 首地址，即 FString 首地址 + 0x0）
	//    - Num（int32）：偏移 0x4（DataPtr 占 4 字节，紧跟其后）
	//    - Capacity（int32）：偏移 0x8（Num 占 4 字节，紧跟其后）
	//    - TArray 总大小：0xC（12 字节）→ FString 总大小 = 0xC
	//
	// 2. 64位环境（指针占 8 字节，int32 占 4 字节，自动对齐到 8 字节）：
	//    - DataPtr（TCHAR*）：偏移 0x0（相对于 Data 首地址，即 FString 首地址 + 0x0）
	//    - Num（int32）：偏移 0x8（DataPtr 占 8 字节，紧跟其后，无填充）
	//    - Capacity（int32）：偏移 0xC（Num 占 4 字节，紧跟其后，0x8+0x4=0xC）
	//    - 对齐补充：0xC 到 0x10 无填充（因 0xC + 0x4 = 0x10，满足 8 字节对齐）
	//    - TArray 总大小：0x10（16 字节）→ FString 总大小 = 0x10
	// -------------------------------------------------------------------------------------------------------------------

	// 编译期类型检查Trait（无内存偏移，仅确保类型安全）
	template <typename RangeType>
	using TRangeElementType = typename TRemoveCV<typename TRemovePointer<decltype(GetData(DeclVal<RangeType>()))>::Type>::Type;

	template <typename CharRangeType>
	struct TIsRangeOfCharType : TIsCharType<TRangeElementType<CharRangeType>>
	{
	};

	template <typename CharRangeType>
	struct TIsRangeOfTCHAR : TIsSame<TCHAR, TRangeElementType<CharRangeType>>
	{
	};

	template <typename CharRangeType>
	using TIsCharRangeNotCArray = TAnd<
		TIsContiguousContainer<CharRangeType>,
		TNot<TIsArray<typename TRemoveReference<CharRangeType>::Type>>,
		TIsRangeOfCharType<CharRangeType>>;

	template <typename CharRangeType>
	using TIsTCharRangeNotCArray = TAnd<
		TIsContiguousContainer<CharRangeType>,
		TNot<TIsArray<typename TRemoveReference<CharRangeType>::Type>>,
		TIsRangeOfTCHAR<CharRangeType>>;

public:
	using ElementType = TCHAR;

	// 构造函数（无内存偏移，仅逻辑实现）
	FString() = default;
	FString(FString&&) = default;
	FString(const FString&) = default;
	FString& operator=(FString&&) = default;
	FString& operator=(const FString&) = default;

	/**
	 * 带额外内存的拷贝构造
	 * @param Other 源字符串
	 * @param ExtraSlack 额外预分配字符数
	 * 内存影响：仅修改 Data（TArray）的 Capacity，不改变 FString 成员偏移
	 */
	FORCEINLINE FString(const FString& Other, int32 ExtraSlack)
		: Data(Other.Data, ExtraSlack + ((Other.Data.Num() || !ExtraSlack) ? 0 : 1))
	{
	}

	/** 右值版本带额外内存构造：仅转移 Data 资源，偏移不变 */
	FORCEINLINE FString(FString&& Other, int32 ExtraSlack)
		: Data(MoveTemp(Other.Data), ExtraSlack + ((Other.Data.Num() || !ExtraSlack) ? 0 : 1))
	{
	}

	/**
	 * 从C风格字符数组构造
	 * @param Src C风格字符数组（需null终止）
	 * 内存影响：初始化 Data 的 DataPtr（分配字符内存）、Num（字符数+1）、Capacity（至少 Num），偏移仍为 0x0
	 */
	template <
		typename CharType,
		typename = typename TEnableIf<TIsCharType<CharType>::Value>::Type
	>
	FORCEINLINE FString(const CharType* Src)
	{
		if (Src && *Src)
		{
			int32 SrcLen = TCString<CharType>::Strlen(Src) + 1;
			int32 DestLen = FPlatformString::ConvertedLength<TCHAR>(Src, SrcLen);
			Data.Reserve(DestLen);  // 修改 Data.Capacity（偏移 0x8/0xC）
			Data.AddUninitialized(DestLen);  // 修改 Data.DataPtr（偏移 0x0）和 Data.Num（偏移 0x4/0x8）

			FPlatformString::Convert(Data.GetData(), DestLen, Src, SrcLen);
		}
	}

	// 其他构造函数、运算符重载、成员函数（均不改变 FString 成员偏移，仅操作 Data 内部数据）
	// ...（省略其余函数实现，核心偏移已在 Data 成员处说明）
};

// ###########################################################################
// FString 内存偏移总结表（基于 UE 4.x/5.x 默认编译配置）
// ###########################################################################
| 层级                | 成员/结构          | 32位偏移（相对于FString首地址） | 64位偏移（相对于FString首地址） | 偏移原因                                                                 |
|---------------------|--------------------|--------------------------------|--------------------------------|------------------------------------------------------------------------|
| FString 实例        | 无虚表指针         | -                              | -                              | FString 无虚函数，不生成隐藏虚表指针，成员从 0x0 开始。                       |
| FString 唯一成员    | Data（TArray<TCHAR>）| 0x0                            | 0x0                            | FString 仅含此成员，无任何前导填充，成员首地址 = FString 实例首地址。           |
| TArray<TCHAR> 内部  | DataPtr（TCHAR*）   | 0x0                            | 0x0                            | TArray 第一个成员，指针占 4/8 字节，从 TArray 首地址（FString 0x0）开始。     |
| TArray<TCHAR> 内部  | Num（int32）        | 0x4                            | 0x8                            | 32位：紧跟 DataPtr（4字节）；64位：紧跟 DataPtr（8字节），无填充。              |
| TArray<TCHAR> 内部  | Capacity（int32）   | 0x8                            | 0xC                            | 32位：紧跟 Num（4字节）；64位：紧跟 Num（4字节），0x8+0x4=0xC，满足对齐。       |
| FString 总大小      | -                  | 0xC（12字节）                  | 0x10（16字节）                 | 等于 TArray<TCHAR> 大小，无额外成员占用。                                     |

// 重要提醒：
// 1. 偏移依赖 TArray 实现：UE 版本若修改 TArray 结构（如新增成员），FString 偏移会同步变化（4.x/5.x 无此问题）。
// 2. 字符数据存储：Data.DataPtr 是指向堆内存的指针（存储实际字符，如 "Hello" 的 'H','e','l','l','o','\0'），其地址需通过解引用获取，非 FString 实例内偏移。
// 3. 禁止硬编码偏移：若需动态获取，建议用 UE 内置函数（如 GetData()、Len()），避免依赖固定偏移导致版本兼容问题。

```

## 4. 4.UE-探索GetName的加密算法（二）GName（GName在代码中是什么和Blocks字符串存放地）

- URL: https://jisuanjiwang.blog.csdn.net/article/details/152007719
- Description: æç« æµè§éè¯»2.1kæ¬¡ï¼ç¹èµ20æ¬¡ï¼æ¶è26æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ ue èå¹» UnrealEngine_getdisplayindex

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：3.UE-探索GetName的加密算法（一）-GName（FName和UObjectBase结构） 
上一个内容中可以找到FName了，也就是通过得到UObjectBase类的地址，使用UObjectBase类的地址+十六进制数18，就可以得到了，然后接下来是FName里的ToString()函数，也就是下图红框的函数，然后按着CTRL鼠标左键单击下图红框位置 
 
进入ToString函数 
 
然后NAME_NO_NUMBER_INTERNAL的值是0 
 
也就是说GetNumber函数返回0才会执行if里面的代码 
 
也就是执行下图红框的代码 
 
代码说明(ai生成)

```text
// 将FName转换为FString（可读字符串）
// FName是UE中高效存储和比较的字符串类型（通过全局字符串表+索引实现），ToString()用于获取其人类可读的字符串形式
FString FName::ToString() const
{
	// 判断FName是否包含数字后缀（FName支持同名带数字区分，如"Mesh_1"、"Mesh_2"）
	// NAME_NO_NUMBER_INTERNAL是内部常量，表示"没有数字后缀"
	if (GetNumber() == NAME_NO_NUMBER_INTERNAL)
	{
		// 无数字后缀的优化路径：直接返回名称条目中的纯字符串
		// 为什么这样优化？
		// - 避免创建临时FString再拼接（无数字时无需额外处理）
		// - GetDisplayNameEntry()获取FName在全局字符串表中的条目（存储原始字符串）
		// - GetPlainNameString()返回条目中的基础字符串（不含数字后缀）
		return GetDisplayNameEntry()->GetPlainNameString();
	}
	
	// 有数字后缀的情况：需要拼接基础字符串和数字
	FString Out;	// 用于存储结果的空FString
	ToString(Out);	// 调用重载版本，将基础字符串和数字拼接后存入Out
	return Out;		// 返回拼接后的结果
}

```
 
接下来先看GetDisplayNameEntry函数，如下图 
 
代码说明

```text
// 获取当前FName在全局名字池中的显示条目（包含实际字符串数据）
// FNameEntry：存储字符串原始数据的结构体（如"Player"、"Mesh"等基础字符串）
// 作用：通过该条目可获取FName对应的可读字符串（用于ToString()等场景）
const FNameEntry* FName::GetDisplayNameEntry() const
{
	// 步骤拆解：
	// 1. GetNamePool()：获取UE全局的名字池（FNamePool单例）
	//    - 名字池是所有FName共享字符串的中央仓库，确保相同字符串只存储一次（节省内存）
	// 2. GetDisplayIndex()：获取当前FName用于显示的索引（指向名字池中的具体条目）
	//    - FName内部通过索引关联名字池，而非直接存储字符串，这是其高效性的核心（快速比较、低内存占用）
	// 3. Resolve(Index)：名字池的方法，通过索引查找并返回对应的FNameEntry引用
	// 4. &取地址：将引用转换为指针，作为函数返回值
	return &GetNamePool().Resolve(GetDisplayIndex());
}

```
 
然后先看GetNamePool函数，它的作用就是为了返回NamePoolData 
 
代码说明，这个NamePoolData就是所谓的GName，说白了GName就是一个FNamePool类型的全局变量，具体代码的实现就是NamePoolData

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：3.UE-探索GetName的加密算法（一）-GName（FName和UObjectBase结构） 
上一个内容中可以找到FName了，也就是通过得到UObjectBase类的地址，使用UObjectBase类的地址+十六进制数18，就可以得到了，然后接下来是FName里的ToString()函数，也就是下图红框的函数，然后按着CTRL鼠标左键单击下图红框位置 
 
进入ToString函数 
 
然后NAME_NO_NUMBER_INTERNAL的值是0 
 
也就是说GetNumber函数返回0才会执行if里面的代码 
 
也就是执行下图红框的代码 
 
代码说明(ai生成) 

```text
// 将FName转换为FString（可读字符串）
// FName是UE中高效存储和比较的字符串类型（通过全局字符串表+索引实现），ToString()用于获取其人类可读的字符串形式
FString FName::ToString() const
{
	// 判断FName是否包含数字后缀（FName支持同名带数字区分，如"Mesh_1"、"Mesh_2"）
	// NAME_NO_NUMBER_INTERNAL是内部常量，表示"没有数字后缀"
	if (GetNumber() == NAME_NO_NUMBER_INTERNAL)
	{
		// 无数字后缀的优化路径：直接返回名称条目中的纯字符串
		// 为什么这样优化？
		// - 避免创建临时FString再拼接（无数字时无需额外处理）
		// - GetDisplayNameEntry()获取FName在全局字符串表中的条目（存储原始字符串）
		// - GetPlainNameString()返回条目中的基础字符串（不含数字后缀）
		return GetDisplayNameEntry()->GetPlainNameString();
	}
	
	// 有数字后缀的情况：需要拼接基础字符串和数字
	FString Out;	// 用于存储结果的空FString
	ToString(Out);	// 调用重载版本，将基础字符串和数字拼接后存入Out
	return Out;		// 返回拼接后的结果
}

```
 
接下来先看GetDisplayNameEntry函数，如下图 
 
代码说明 

```text
// 获取当前FName在全局名字池中的显示条目（包含实际字符串数据）
// FNameEntry：存储字符串原始数据的结构体（如"Player"、"Mesh"等基础字符串）
// 作用：通过该条目可获取FName对应的可读字符串（用于ToString()等场景）
const FNameEntry* FName::GetDisplayNameEntry() const
{
	// 步骤拆解：
	// 1. GetNamePool()：获取UE全局的名字池（FNamePool单例）
	//    - 名字池是所有FName共享字符串的中央仓库，确保相同字符串只存储一次（节省内存）
	// 2. GetDisplayIndex()：获取当前FName用于显示的索引（指向名字池中的具体条目）
	//    - FName内部通过索引关联名字池，而非直接存储字符串，这是其高效性的核心（快速比较、低内存占用）
	// 3. Resolve(Index)：名字池的方法，通过索引查找并返回对应的FNameEntry引用
	// 4. &取地址：将引用转换为指针，作为函数返回值
	return &GetNamePool().Resolve(GetDisplayIndex());
}

```
 
然后先看GetNamePool函数，它的作用就是为了返回NamePoolData 
 
代码说明，这个NamePoolData就是所谓的GName，说白了GName就是一个FNamePool类型的全局变量，具体代码的实现就是NamePoolData 

```text
// 获取全局唯一的名字池（FNamePool）实例
// FNamePool是UE管理所有FName字符串的"中央仓库"，所有FName的基础字符串都存在这里，确保不重复存储
static FNamePool& GetNamePool()
{
    // 第一步：检查名字池是否已经初始化过
    if (bNamePoolInitialized)  // bNamePoolInitialized是个全局标志，true表示已经创建过名字池
    {
        // 如果已经初始化，直接返回已有的名字池实例
        // NamePoolData是存储名字池的内存地址，把它转成FNamePool指针后，返回它的引用
        return *(FNamePool*)NamePoolData;
    }

    // 第二步：如果没初始化，创建名字池实例
    // 这里用了特殊的new（placement new）：不在新地址创建对象，而是在NamePoolData预分配的内存里创建
    // 为什么这么做？避免动态分配内存的开销，确保名字池在固定地址，更高效、安全
    FNamePool* Singleton = new (NamePoolData) FNamePool;  // 在指定内存创建FNamePool对象
    
    bNamePoolInitialized = true;  // 标记为已初始化，下次调用直接返回已有实例
    return *Singleton;  // 返回新创建的名字池实例的引用
}

```
 
它的定义 
 
代码说明，这个GName的内存地址找法后面会写 

```text
// 为全局名字池（FNamePool）预分配的静态内存缓冲区
// 作用：给GName（全局唯一的FNamePool实例）提供固定的存储位置，避免动态内存分配的开销和风险
// 逐部分解析：
// 1. alignas(FNamePool)：
//    - 强制内存对齐，确保NamePoolData的起始地址符合FNamePool类的对齐要求（如8字节、16字节对齐）
//    - 为什么需要对齐？CPU访问内存时，对特定地址（如8的倍数）的访问效率更高，不对齐可能导致性能下降或崩溃
//    - FNamePool内部有指针、大数组等成员，必须对齐才能正确构造和使用
//
// 2. static uint8：
//    - static：静态变量，意味着这块内存从程序启动到退出一直存在，不会被中途释放（适合全局唯一的名字池）
//    - uint8：无符号字节类型，这里用于表示"原始内存块"（类似一堆连续的字节容器）
//
// 3. NamePoolData[sizeof(FNamePool)]：
//    - NamePoolData：数组名，标识这块内存是专门给名字池用的
//    - [sizeof(FNamePool)]：数组大小正好等于FNamePool类的字节大小（用sizeof计算）
//    - 确保内存块能完整容纳一个FNamePool对象（不多不少，刚好够用）
//
// 关联逻辑：
// 当GetNamePool()第一次调用时，会用"placement new"在这块内存中构造FNamePool实例（GName）
// 这种方式比普通new更高效：无需动态申请内存，地址固定，且避免内存碎片
alignas(FNamePool) static uint8 NamePoolData[sizeof(FNamePool)];

```
 
然后GetNamePool函数就看完了，接下来是&GetNamePool().Resolve(GetDisplayIndex())中的GetDisplayIndex函数，如下图它返回了一个Index，Index的值来自于GetDisplayIndexFast函数 
 
代码说明 

```text
// 获取当前FName在名字池中的"显示索引"（带有效性检查）
// FNameEntryId：用于标识名字池中FNameEntry的ID类型（本质是索引，类似数组下标）
// 作用：返回FName对应的全局名字池条目索引，确保该索引有效（避免访问无效内存）
FORCEINLINE FNameEntryId GetDisplayIndex() const
{
    // 1. 快速获取索引：调用GetDisplayIndexFast()直接返回内部存储的索引值
    //    为什么叫"Fast"？因为这个函数不做有效性检查，单纯返回值，速度更快
    const FNameEntryId Index = GetDisplayIndexFast();

    // 2. 验证索引有效性：
    //    - IsWithinBounds(Index)：检查索引是否在名字池的有效范围内（比如不超过当前最大条目数）
    //    - checkName()：UE的断言宏（仅在调试模式生效），如果索引无效会触发错误并中断程序
    //    作用：确保返回的索引能正确指向名字池中的FNameEntry（避免访问空指针或越界）
    checkName(IsWithinBounds(Index));

    // 3. 返回经过验证的有效索引
    return Index;
}

```
 
然后进入GetDisplayIndexFast函数 
 
代码说明：开发的时候会使用DisplayIndex，因为开发时不需要区分大小写，区分大小写后反而会麻烦，游戏开发完后发布时会使用ComparisonIndex 

```text
// 快速获取FName的"显示索引"（不做有效性检查，仅返回内部存储的索引值）
// FNameEntryId：名字池中条目的唯一标识（类似数组下标）
// 作用：在性能敏感场景下，直接返回FName内部存储的索引，跳过检查以提升速度
FORCEINLINE FNameEntryId GetDisplayIndexFast() const
{
    // 条件编译：会根据引擎是否开启"大小写保留"功能，返回不同的索引
#if WITH_CASE_PRESERVING_NAME
    // 当开启大小写保留（WITH_CASE_PRESERVING_NAME为真）时：
    // 返回DisplayIndex（对应原始大小写的字符串条目索引，如"Player"和"player"是不同条目）
    return DisplayIndex;
#else
    // 当不开启大小写保留（默认情况）时：
    // 返回ComparisonIndex（对应大小写不敏感的字符串条目索引，如"Player"和"player"会映射到同一个条目）
    return ComparisonIndex;
#endif
}

```
 
然后注意按着CTRL鼠标单击下图红框时 
 
会出现两个选择 
 
我们要看的是909这一行的 
 
因为909这一行离着我们找到的GetDisplayIndexFast函数最近 
 
然后ComparisonIndex和DisplayIndex它们的声明都一样的，这俩看哪一个应该都可以，这里看ComparisonIndex 
 
然后ComparisonIndex在FName类里，FName里的代码很长，从下图中可以看到FName在401行，距离ComparisonIndex相差500多行，然后FName里面没有虚函数，ComparisonIndex是FName的第一个成员变量，这就是FName+0x0位置是ComparisonIndex 
 
然后GetDisplayIndex就看完了，然后是&GetNamePool().Resolve(GetDisplayIndex())里面的Resolve函数 
 
然后它的入参是FNameEntryHandle类型，但是我们给它传的是FNameEntryId类型 
 
这个类型的转换是在FNameEntryHandle里，通过下图红框FNameEntryHandle的构造函数里转换的 
 
通过Block(Id.ToUnstableInt() >> FNameBlockOffsetBits)这样的写法把值赋值给Block变量，也就是赋值给下图红框的变量 
 
然后通过Offset(Id.ToUnstableInt() & (FNameBlockOffsets - 1))这样的方式赋值给Offset变量，也就是下图红框的变量 
 
然后下图红框函数 
 
它直接返回了一个Value，也就是一个int 
 
然后还有一个右移的操作，把Id.ToUnstableInt()的值右移16位，比如ToUnstableInt返回的数字的二进制是10000000000000000，它有17位也就是有17个数字，右移16位就变成了00000000000000001，也就是把1右边16个数字全部删除，然后左边补充16个0，从而让它保持17位，然后这是Block的值 
 
然后是Offset的值是先左移（和右移一样只是它俩的操作是反着的，它是删除左边，右边补0），然后还进行一个&运算，&运算是，现在有两个二进制一个是100010，另一个是100000，经过&运算会变成100000，也就是都是1才是1 
 
然后FNameEntryId转FNameEntryHandle就看完了，然后是Entries.Resolve(Handle)里的Resolve 
 
代码说明 

```text
// 通过 FNameEntryHandle（句柄）查找并返回对应的 FNameEntry（字符串条目）引用
// 作用：将“块索引+块内偏移”的定位信息转换为实际的字符串条目，是名字池中获取条目数据的核心函数
// 参数：Handle - 包含 Block（块索引）和 Offset（块内偏移）的定位句柄
FNameEntry& Resolve(FNameEntryHandle Handle) const
{
	// Lock not needed（无需加锁）
	// 原因：此函数通常在单线程上下文调用，或名字池已通过其他机制保证线程安全，
	// 省去加锁解锁的开销以提升性能（FName操作是高频场景，性能至关重要）

	// 计算 FNameEntry 在内存中的实际地址：
	// 1. Blocks[Handle.Block] → 获取第 Handle.Block 个“块”的起始内存地址（类似“第N个书架的第一个格子地址”）
	// 2. Stride * Handle.Offset → 计算块内偏移量：Stride 是每个 FNameEntry 占用的内存大小（类似“每个格子的宽度”），
	//    乘以 Offset（第几个格子）得到从块起始地址到目标条目的距离
	// 3. 两者相加 → 目标 FNameEntry 的内存地址（书架起始地址 + 格子距离 = 具体格子地址）
	// 4. reinterpret_cast<FNameEntry*> → 将计算出的地址转换为 FNameEntry 指针（告诉编译器这是一个字符串条目的地址）
	// 5. * → 解引用指针，得到 FNameEntry 的引用（直接操作条目数据）
	return *reinterpret_cast<FNameEntry*>(Blocks[Handle.Block] + Stride * Handle.Offset);
}

```
 
然后是下图红框的两个值的来源 
 
Stride的值取决于FNameEntry类型的大小 
 
是4字节，Stride的值就是4 
 
然后是Blocks的值，它存储了游戏中所有的字符串，也就是在游戏中看到的文字 
 
代码说明 

```text
// 这行代码定义了一个“块地址数组”，是名字池（FNamePool）管理分块存储的核心结构
// 作用：像“图书馆的书架地址目录”一样，记录所有存储字符串条目的“块”在内存中的起始位置
uint8* Blocks[FNameMaxBlocks] = {};

// 小白版逐句解释：
// 1. uint8* → “指向内存字节的指针”
//    - 可以理解为“内存地址”（比如0x123456），指向一块连续的内存空间的开头
//    - 这里每个指针都对应一个“块”（Block）的起始地址（类似“第3个书架从图书馆的哪个位置开始”）

// 2. Blocks → 数组的名字，意思是“所有块的集合”
//    - 你可以把它想象成一本“目录册”，每一页记录一个块的起始地址

// 3. [FNameMaxBlocks] → 数组的大小
//    - FNameMaxBlocks 是一个固定的数字（比如1024），表示这个目录册最多能记录多少个块的地址
//    - 相当于“图书馆最多能放1024个书架”，目录册就只有1024页

// 4. = {} → 初始化数组，把所有指针都设为“空”（nullptr）
//    - 刚创建名字池时，还没有任何块，所以目录册的所有页面都是空白的
//    - 防止指针指向随机的无效内存（避免程序崩溃）

// 为什么需要这个数组？
// 名字池里的字符串条目（FNameEntry）太多了，被分成了很多“块”（比如每个块存65536个条目）。
// 当需要找某个条目时：
// 1. 先通过 FNameEntryHandle 知道它在“第2个块”（Handle.Block = 2）
// 2. 查这个 Blocks 数组，Blocks[2] 就是第2个块的起始地址（比如0x789000）
// 3. 再用块内偏移（Handle.Offset）算出具体位置，就能快速找到条目

// 简单说：这个数组就是“块的地址目录”，让程序不用瞎找，直接按索引拿地址，速度飞快！

```
 
Blocks和Stride它们都在FNameEntryAllocator类中 
 
然后Blocks是比较重要的，然后它的偏移，在Blocks前面有下图红框的变量，它的大小是8 
 
为什么说FRWLock是8，一步一步看，如下图进入FRWLock 
 
然后进入FWindowsRWLock，它里面就只有下图红框一个变量 
 
然后SRWLOCK里只有一个void*类型，这个类型在64位下是8字节，32位是4字节，所以说Lock是8字节 
 
Blocks的位置是FNameEntryAllocator首地址+8+4+4，8+4+4的结果是16，16的十六机制是10，然后FNameEntryAllocator在FNamePool（GName）里 
 
Entries在FNamePool中第一个，所以想得到Blocks的公式是首先取出FNamePool第0位的数据，这个数据是一个内存地址，内存地址里的数据是FNameEntryAllocator结构的首地址，也就是得到FNameEntryAllocator的数据，然后再进行8+4+4得到Blocks，得到Blocks后再通过 Blocks[Handle.Block] + Stride * Handle.Offset 这个算法得到一个地址（字符串的内存地址）。

## 5. 5.UE-探索GetName的加密算法（三）GName（手动使用GName算法，算法总结）

- URL: https://jisuanjiwang.blog.csdn.net/article/details/152048834
- Description: æç« æµè§éè¯»2kæ¬¡ï¼ç¹èµ16æ¬¡ï¼æ¶è49æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ ue GName UnrealEngine èå¹»å¼æ_gnameç®æ³

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：4.UE-探索GetName的加密算法（二）GName（GName在代码中是什么和Blocks字符串存放地） 
上一个内容里写的Stride是4，这个有点不正确，它只有在开发的时候才会是4 
 
然后下图红框alignof是取FNameEntry类的内存对齐的方式 
 
下图红框里有一个WITH_CASE_PRESERVING_NAME，开发的时候它才会存在，它存在也就导致ComparisonId是存在的，ComparisonId是4字节，然后在FNameEntry4字节是最大的，所以会使用4字节对齐 
 
然后FNameEntryHeader的大小，它里面只会有一个int16，int16这个类型是2字节 
 
所以如果ComparisonId不存在（非开发），下图红框的两个是最大的，它们都是2字节 
 
所以现在下图红框的算法是*reinterpret_cast<FNameEntry*>(Blocks[Handle.Block] + 2 * Handle.Offset) 
 
然后到这下图红框的GetDisplayNameEntry函数就分析好了 
 
接下来是下图红框的GetPlainNameString函数 
 
进入GetPlainNameString函数 
 
代码说明

```text
// 函数功能：从当前FNameEntry中取出存储的字符串内容，转换成UE引擎中常用的FString类型并返回
// 简单说：这个函数就是"把FNameEntry里存的字符串取出来，变成可以直接用的字符串类型"
FString FNameEntry::GetPlainNameString() const
{
    // 创建一个临时缓冲区（FNameBuffer是UE定义的结构体，里面有两个数组，分别用来临时存ANSI字符和宽字符）
    // 作用：就像一个"临时托盘"，先把从FNameEntry里取出来的原始字符数据放在这里，方便后续处理
    FNameBuffer Temp;

// 检查当前FNameEntry存储的是宽字符（WIDECHAR）还是ANSI字符（ANSICHAR）
    // Header是FNameEntry里的"标签结构体"，bIsWide是标签里的一个标识位（1表示宽字符，0表示ANSI字符）
    if (Header.bIsWide)
    {
        // 如果是宽字符：
        // 1. 调用GetUnterminatedName(Temp.WideName)：从当前FNameEntry中取出"没有加结束符的原始宽字符数据"，存到临时缓冲区的WideName数组里
        //    （注：计算机里字符串通常以'\0'作为结束标志，这里"未加结束符"指的是原始存储的字符本身，还没补这个标志）
        // 2. 用FString的构造函数：根据字符串长度（Header.Len）和刚才取到的原始宽字符数据，创建一个FString并返回
        return FString(Header.Len, GetUnterminatedName(Temp.WideName));
    }
    else
    {
        // 如果是ANSI字符：
        // 逻辑和宽字符类似，只是取的是ANSI字符数据，存到临时缓冲区的AnsiName数组里
        // 最后用这些数据创建FString并返回
        return FString(Header.Len, GetUnterminatedName(Temp.AnsiName));
    }
}

```
 
然后GetPlainNameString函数里主要就是复制内存，然后把创建的内存搞成一个FString类型，复制的操作在下图红框GetUnterminatedName函数中 
 
GetUnterminatedName函数 
 
代码说明

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：4.UE-探索GetName的加密算法（二）GName（GName在代码中是什么和Blocks字符串存放地） 
上一个内容里写的Stride是4，这个有点不正确，它只有在开发的时候才会是4 
 
然后下图红框alignof是取FNameEntry类的内存对齐的方式 
 
下图红框里有一个WITH_CASE_PRESERVING_NAME，开发的时候它才会存在，它存在也就导致ComparisonId是存在的，ComparisonId是4字节，然后在FNameEntry4字节是最大的，所以会使用4字节对齐 
 
然后FNameEntryHeader的大小，它里面只会有一个int16，int16这个类型是2字节 
 
所以如果ComparisonId不存在（非开发），下图红框的两个是最大的，它们都是2字节 
 
所以现在下图红框的算法是*reinterpret_cast<FNameEntry*>(Blocks[Handle.Block] + 2 * Handle.Offset) 
 
然后到这下图红框的GetDisplayNameEntry函数就分析好了 
 
接下来是下图红框的GetPlainNameString函数 
 
进入GetPlainNameString函数 
 
代码说明 

```text
// 函数功能：从当前FNameEntry中取出存储的字符串内容，转换成UE引擎中常用的FString类型并返回
// 简单说：这个函数就是"把FNameEntry里存的字符串取出来，变成可以直接用的字符串类型"
FString FNameEntry::GetPlainNameString() const
{
    // 创建一个临时缓冲区（FNameBuffer是UE定义的结构体，里面有两个数组，分别用来临时存ANSI字符和宽字符）
    // 作用：就像一个"临时托盘"，先把从FNameEntry里取出来的原始字符数据放在这里，方便后续处理
    FNameBuffer Temp;

    // 检查当前FNameEntry存储的是宽字符（WIDECHAR）还是ANSI字符（ANSICHAR）
    // Header是FNameEntry里的"标签结构体"，bIsWide是标签里的一个标识位（1表示宽字符，0表示ANSI字符）
    if (Header.bIsWide)
    {
        // 如果是宽字符：
        // 1. 调用GetUnterminatedName(Temp.WideName)：从当前FNameEntry中取出"没有加结束符的原始宽字符数据"，存到临时缓冲区的WideName数组里
        //    （注：计算机里字符串通常以'\0'作为结束标志，这里"未加结束符"指的是原始存储的字符本身，还没补这个标志）
        // 2. 用FString的构造函数：根据字符串长度（Header.Len）和刚才取到的原始宽字符数据，创建一个FString并返回
        return FString(Header.Len, GetUnterminatedName(Temp.WideName));
    }
    else
    {
        // 如果是ANSI字符：
        // 逻辑和宽字符类似，只是取的是ANSI字符数据，存到临时缓冲区的AnsiName数组里
        // 最后用这些数据创建FString并返回
        return FString(Header.Len, GetUnterminatedName(Temp.AnsiName));
    }
}

```
 
然后GetPlainNameString函数里主要就是复制内存，然后把创建的内存搞成一个FString类型，复制的操作在下图红框GetUnterminatedName函数中 
 
GetUnterminatedName函数 
 
代码说明 

```text
// 函数功能：获取当前FNameEntry中存储的"未加终止符的宽字符字符串"（宽字符即WIDECHAR，通常用于存储中文、日文等多字节字符）
// FORCEINLINE：UE的宏，强制编译器把这个函数的代码"直接嵌入到调用它的地方"（而不是像普通函数那样跳转执行），目的是减少函数调用的开销，让程序运行更快
// 返回值：指向宽字符字符串的指针（const表示不能通过这个指针修改字符串内容）
FORCEINLINE const WIDECHAR* FNameEntry::GetUnterminatedName(WIDECHAR(&OptionalDecodeBuffer)[NAME_SIZE]) const
{
    // 如果定义了"WITH_CUSTOM_NAME_ENCODING"这个宏（表示项目启用了"自定义名字编码"功能，比如加密或特殊格式存储字符串）
#ifdef WITH_CUSTOM_NAME_ENCODING
    // 1. 调用CopyUnterminatedName函数：把FNameEntry里存储的宽字符字符串（可能是加密/特殊编码的）复制到传入的临时缓冲区OptionalDecodeBuffer中，同时完成解码
    // 2. OptionalDecodeBuffer：一个宽字符数组（大小为NAME_SIZE），作为"临时容器"接收解码后的字符串
    CopyUnterminatedName(OptionalDecodeBuffer);
    // 返回这个临时缓冲区的地址，里面就是解码后、未加终止符的宽字符字符串
    return OptionalDecodeBuffer;
#else
    // 如果没有启用自定义编码（默认情况），直接返回FNameEntry内部存储宽字符的数组WideName
    // WideName是FNameEntry里的联合体成员，直接存储原始宽字符数据，没有加密或特殊处理
    return WideName;
#endif
}
// 关键概念补充：
// 1. 未加终止符（Unterminated）：
//    计算机中字符串通常以'\0'（空字符）作为结束标志（类似句子的句号）
//    这里的"未加终止符"指字符串内容本身没有这个'\0'，只包含有效字符
//    原因：FNameEntry为了节省内存，存储时可能省略结束符，使用时通过Header.Len知道长度
// 2. 宽字符（WIDECHAR）与ANSI字符：
//    - ANSI字符：1字节/个，只能存英文、数字等（类似"小盒子"）
//    - WIDECHAR：2字节/个，能存中文、日文等（类似"大盒子"，容纳更多字符）
// 3. 缓冲区（OptionalDecodeBuffer）的作用：
//    当字符串有特殊编码时，不能直接返回原始数据（可能是乱码或加密内容）
//    因此先解码到临时缓冲区，再返回缓冲区地址，确保调用者拿到的是正确的字符串

```
 
然后CopyUnterminatedName如下图红框 
 
代码说明 

```text
// 函数功能：将当前FNameEntry中存储的宽字符字符串（未加终止符）复制到目标缓冲区，并进行解码（如果有特殊编码的话）
// 简单说：就是把内部的宽字符内容"复制粘贴"到外面的缓冲区，再做必要的解密/还原处理

// 函数声明拆解：
// 1. void：函数没有返回值（只负责"做事"，不返回结果）
// 2. FNameEntry::CopyUnterminatedName：属于FNameEntry类的成员函数，函数名意思是"复制未加终止符的名字"
// 3. (WIDECHAR* Out)：函数的参数
//    - WIDECHAR*：指向宽字符的指针（表示"目标缓冲区的地址"，告诉函数要把内容复制到哪里）
//    - Out：参数名，意为"输出"，即复制的结果会存到这里
// 4. const：函数末尾的const，表示这个函数不会修改FNameEntry自身的数据（只读取内部的宽字符内容）

void FNameEntry::CopyUnterminatedName(WIDECHAR* Out) const
{
    // 第一步：把内部存储的宽字符数据复制到目标缓冲区Out中
    // FPlatformMemory::Memcpy：UE封装的内存复制函数，作用类似"Ctrl+C再Ctrl+V"，直接复制内存中的二进制数据
    // 参数说明：
    // - 第一个参数Out：目标地址（要粘贴到哪里）
    // - 第二个参数WideName：源地址（要复制的内容在哪里，FNameEntry内部存储宽字符的数组）
    // - 第三个参数：要复制的字节数 = 每个宽字符的大小 × 字符串长度
    //   - sizeof(WIDECHAR)：每个宽字符占2字节（因为WIDECHAR是2字节类型）
    //   - Header.Len：字符串的长度（从Header中获取，比如长度为5表示有5个宽字符）
    //   举例：如果字符串长度是3，就需要复制 2×3=6字节的数据
    FPlatformMemory::Memcpy(Out, WideName, sizeof(WIDECHAR) * Header.Len);

    // 第二步：对复制到Out缓冲区的字符串进行解码
    // Decode是内部函数，作用是还原特殊编码的字符串（比如如果存储时加密了，这里就解密；如果压缩了，这里就解压）
    // 参数：Out（要解码的字符串）、Header.Len（字符串长度，告诉解码函数要处理多少个字符）
    Decode(Out, Header.Len);
}

// 关键概念解释：
// 1. 为什么用Memcpy？
//    因为要直接复制原始的宽字符数据（二进制层面的复制），比逐个字符复制更快，尤其适合频繁调用的场景

// 2. 为什么要计算字节数？
//    Memcpy需要明确知道要复制多少字节的内容。宽字符每个占2字节，所以"总字节数 = 单个大小 × 字符数量"，确保不多复制也不少复制

// 3. 解码（Decode）的意义？
//    如果项目启用了自定义编码（比如WITH_CUSTOM_NAME_ENCODING宏开启），字符串存储时可能被加密或特殊处理（节省空间或保护数据）
//    这里的解码就是把这些处理过的字符串还原成正常可读的内容，让外部调用者能正确使用

// 4. 为什么是"未加终止符"？
//    复制的字符数量是Header.Len（有效字符数），没有在末尾加'\0'（结束符），因为调用这个函数的地方会根据Header.Len知道字符串长度，不需要结束符

```
 
然后Memcpy函数 
 
代码说明 

```text
// 函数功能：将一块内存中的数据从源地址复制到目标地址，本质是对标准库memcpy函数的封装
// 简单说：就像"文件复制"一样，把一块内存里的内容原封不动地复制到另一块内存，支持复制大块数据

// 函数声明拆解：
// 1. static：静态函数，意味着它属于定义它的类或命名空间，不需要创建对象就能调用（类似"全局工具函数"）
// 2. FORCEINLINE：强制内联编译，把函数代码直接嵌入到调用处（减少函数调用的跳转开销，让复制更快）
// 3. void*：返回值类型，是一个"无类型指针"（可以指向任何类型的内存），返回的是目标地址（Dest）
//    - 作用：方便链式操作（比如复制后直接用这个地址做其他事）
// 4. BigBlockMemcpy：函数名，意为"大块内存复制"（虽然这里直接调用memcpy，但名字暗示它适合处理大块数据）
// 5. 参数列表：
//    - void* Dest：目标内存的起始地址（要复制到哪里，相当于"新文件保存路径"）
//    - const void* Src：源内存的起始地址（要复制的内容在哪里，相当于"原文件路径"）
//    - SIZE_T Count：要复制的字节数（要复制多少数据，相当于"文件大小"，单位是字节）
//    - const修饰Src：表示不会修改源内存的数据（保护原始内容不被意外改动）

static FORCEINLINE void* BigBlockMemcpy(void* Dest, const void* Src, SIZE_T Count)
{
    // 直接调用标准库的memcpy函数完成内存复制
    // memcpy是C/C++的基础内存复制函数，功能是：从Src地址开始，复制Count个字节的数据到Dest地址
    // 这里把memcpy的返回值直接返回（memcpy本身会返回Dest地址）
    return memcpy(Dest, Src, Count);
}

// 关键概念解释：
// 1. 为什么叫"BigBlock"？
//    名字暗示它适合复制"大块内存"（比如几百KB、几MB的数据），但实际实现和普通memcpy一样
//    可能是为了代码可读性（让使用者知道这个函数用于处理大块数据），或预留后续优化空间（比如未来针对大块数据做特殊处理）

// 2. void*指针的意义：
//    void*是"无类型指针"，可以指向任何类型的内存（int、float、字符串等）
//    因为内存复制只关心"字节"，不关心数据是哪种类型，所以用void*更通用（能复制任何类型的数据块）

// 3. 和普通复制的区别：
//    普通复制（比如逐个变量赋值）适合小数据，而内存复制（memcpy/BigBlockMemcpy）直接操作内存，速度极快
//    举例：复制一个1000个元素的数组，用循环逐个复制要1000次操作，用这个函数一次就能完成

// 4. 使用注意：
//    - 目标地址（Dest）和源地址（Src）的内存空间不能重叠（否则可能复制出错误数据）
//    - 目标地址必须有足够的空间（至少能容纳Count个字节，否则会导致内存溢出）

```
 
到这就是GName的算法，很乱这里总结一下 
 
 比如现在的id是123456 
 它的算法是 *reinterpret_cast<FNameEntry*>(Blocks[Handle.Block] + 2 * Handle.Offset) 
 然后Handle.Block的值是id右移16位，也就是下图红框的代码，也就是把右边的2字节删除，然后当做Blocks的索引 
  
 Handle.Offset的值是id& （1左移16位的结果-1）也就是下图红框的代码 
  
 然后1左移16位的结果是65536，然后65536-1=65535 
  
 这个65535是2字节内存空间可以表达的最大数，如下图有16个1，8个1表示1字节，65535的十六进制是FFFF，4个F，从下图中可以看到（HEX就表示的是十六进制数） 
  
 id&65535的算法，比如现在的id是123456789，它的十六进制是75BCD15 
  
 然后进行&运算（也叫and运算） 
  
 运算后，如下图红框它的二进制，123456789的二进制是0111 0101 1011 1100 1101 0001 0101，进行&运算后变成了1100 1101 0001 0101 
  
 &操作是两个二进制数比较都是1才是1，然后FFFF是一个2字节的数，123456789是一个3.5字节的数（二进制有28位，28除以8是3.5，注意这里只是手动计算的实例在计算机中它有内存对齐，它从28会变成32，也就是4字节，不会出现3.5字节这样的东西），也就是把下图红框的数据全部删除了，也就是保留了右边2字节的数据，也就是说Handle.Block保留左边的数据，Handle.Offset保留右边的数据 
  
 现在的算法是 *reinterpret_cast<FNameEntry*>(Blocks[id>>16] + 2 * (id & 65535)，然后它Blocks[id>>16]取出来的数据是一个内存地址，然后2 * (id & 65535)的结果是一个偏移，也就是说比如12345678，Blocks是一个大型图书馆，1234是图书馆里面的书架号，然后Blocks[1234]这个就是找到书架号（内存地址），然后5678乘以2是书在书架中的序号（位置）（内存地址+偏移），然后就能得到文字的数据了，然后再通过下图红框的判断来确定这个文字是什么编码，然后就能得到我们认识的文字了，到这应该就能理解GName的算法了，最开始说的那句话了

## 6. 6.UE-游戏逆向-查找游戏中的GName，查找GName地址

- URL: https://jisuanjiwang.blog.csdn.net/article/details/152091545
- Description: æç« æµè§éè¯»1.3kæ¬¡ï¼ç¹èµ19æ¬¡ï¼æ¶è20æ¬¡ãèå¹» ue4 UnrealEngine æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ _ue4ç4.20.3çæ¬gnamesè¿ä¹

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：5.UE-探索GetName的加密算法（三）GName（手动使用GName算法，算法总结） 
为了防止前三节乱，看不懂先理一下，首先通过搜索GetName(找到了下图的函数，然后下图红框的ToString里面是获取字符串，也就是GName解密 
 
然后通过ToString函数里调用的GetDisplayNameEntry函数就找到了GetNamePool函数，也就是获取GName的函数 
 
然后GetNamePool函数就是获取一个FNamePool类型的变量，FNamePool就是GName，然后根据上图&GetNamePool().Resolve(GetDisplayIndex())这一句代码实际上是调用了GName的Resolve函数 
 
然后通过调用GName的Resolve函数就来到了下图红框位置 
 
然后Resolve函数里面就是使用id找字符串的算法 
 
 
 然后到这就理完了，接下来找GName，首先找GName的原理，是先通过虚幻引擎的源码找一个字符串，然后使用ida反编译工具，对游戏进行反编译，然后在通过ida里面的字符串搜索功能去找从虚幻引擎源码中找到的字符串，找到字符串后就能从ida里定位到代码地址（函数），然后在通过ida里的查找谁调用了当前代码地址就能得到GName的地址了，这句话现在看了会不理解，看完下方的内容就能理解了。 
 
 
首先下图红框的GetNamePool函数的上方static uint8 NamePoolData[sizeof(FNamePool)];是一个全局变量，也就是因为它让我们有了机会找GName的地址，全局变量编程完后内存地址不会有变化，然后怎么找它 
 
按着CTRL鼠标左键单击下图红框，它会跳到FNamePool无参构造函数上 
 
代码说明

```text
// new (NamePoolData) 这是定位new的写法，也就是在创建对象的时候的内存空间，使用NamePoolData它的内存空间
FNamePool* Singleton = new (NamePoolData) FNamePool;

```
 
如下图FNamePool无参构造函数 
 
在它的构造函数里可以看到下图红框的代码，#include的作用，在编译的时候会把文件复制过来，下图红框的意思是把UObject/UnrealNames.inl文件内容插入到1055行，也是因为#include它的作用让我们可以找到GName，也就是调用上图红框函数的位置，从而找到GName 
 
然后下图红框ByteProperty是一个字符串，这是虚幻引擎注册文字的代码 
 
代码说明

```text
// 把字符串"ByteProperty"提前注册到全局名字池（GName）中，
// 并手动指定它的唯一ID是1，后续整个引擎中使用这个字符串都会关联到这个ID
REGISTER_NAME(1, ByteProperty)

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：5.UE-探索GetName的加密算法（三）GName（手动使用GName算法，算法总结） 
为了防止前三节乱，看不懂先理一下，首先通过搜索GetName(找到了下图的函数，然后下图红框的ToString里面是获取字符串，也就是GName解密 
 
然后通过ToString函数里调用的GetDisplayNameEntry函数就找到了GetNamePool函数，也就是获取GName的函数 
 
然后GetNamePool函数就是获取一个FNamePool类型的变量，FNamePool就是GName，然后根据上图&GetNamePool().Resolve(GetDisplayIndex())这一句代码实际上是调用了GName的Resolve函数 
 
然后通过调用GName的Resolve函数就来到了下图红框位置 
 
然后Resolve函数里面就是使用id找字符串的算法 
 
 
 然后到这就理完了，接下来找GName，首先找GName的原理，是先通过虚幻引擎的源码找一个字符串，然后使用ida反编译工具，对游戏进行反编译，然后在通过ida里面的字符串搜索功能去找从虚幻引擎源码中找到的字符串，找到字符串后就能从ida里定位到代码地址（函数），然后在通过ida里的查找谁调用了当前代码地址就能得到GName的地址了，这句话现在看了会不理解，看完下方的内容就能理解了。 
 
 
首先下图红框的GetNamePool函数的上方static uint8 NamePoolData[sizeof(FNamePool)];是一个全局变量，也就是因为它让我们有了机会找GName的地址，全局变量编程完后内存地址不会有变化，然后怎么找它 
 
按着CTRL鼠标左键单击下图红框，它会跳到FNamePool无参构造函数上 
 
代码说明 

```text
// new (NamePoolData) 这是定位new的写法，也就是在创建对象的时候的内存空间，使用NamePoolData它的内存空间
FNamePool* Singleton = new (NamePoolData) FNamePool;

```
 
如下图FNamePool无参构造函数 
 
在它的构造函数里可以看到下图红框的代码，#include的作用，在编译的时候会把文件复制过来，下图红框的意思是把UObject/UnrealNames.inl文件内容插入到1055行，也是因为#include它的作用让我们可以找到GName，也就是调用上图红框函数的位置，从而找到GName 
 
然后下图红框ByteProperty是一个字符串，这是虚幻引擎注册文字的代码 
 
代码说明 

```text
// 把字符串"ByteProperty"提前注册到全局名字池（GName）中，
// 并手动指定它的唯一ID是1，后续整个引擎中使用这个字符串都会关联到这个ID
REGISTER_NAME(1, ByteProperty)

```
 
然后现在就找到了虚幻引擎中的字符串，这个字符串要找一个用的少的，不然调用它的地方太多，使用ida不好找，然后打开游戏的exe所在的目录，然后把exe文件拖到ida的exe上，然后ida会自动反编译游戏的exe文件，如下图游戏的exe文件 
 
如下图红框只要不是数字了，就说明ida加载完成，游戏很大，如图电脑性能不好它可能会加载几个小时 
 
加载完成后，选择Names 
 
然后按CTRL+F，会出现下图红框的输入框 
 
把我们从虚幻引擎源码中复制的字符串粘贴到上图红框里，如下图红框，它最接近我们复制的字符串，不一样的原因可能是编译器搞的，找最接近的就对了，然后鼠标左键直接双击下图红框 
 
然后再双击下图红框位置，就能跳转到使用它的地方 
 
然后下图红框都是汇编代码，不容易分析 
 
按下F5弹出下图弹框，然后点击OK 
 
然后它会把汇编代码搞成伪c++代码（给我参考的c++代码） 
 
如下图红框拿着伪c++代码去对比虚幻引擎的源码，如下图红框，可以很清晰的看出ida里的代码就是UnrealNames.iml文件里的内容 
 
然后上方说#include是把UnrealNames.iml文件里的内容复制到了1055行，把ida里的滚动条拉倒最后，可以看到与虚幻引擎一样的字符串，虽然顺序不一样（这是编译后导致的），但是字符串是一样的，然后就能证明从ida里找到了FNamePool无参构造函数的代码，编译后的代码 
 
然后找到了FNamePool无参构造函数，接下来就找谁调用了它，点击下图红框的菜单 
 
下图红框是调用它的地方，随便双击任意一个 
 
如下图红框通过与虚幻引擎源码对比，它们的代码结构是很相似的，所以就找到了GName的地址，也就是stru_144A56400里的144A56400 
 
144A56400这个值每次游戏打开的时候是不一样的，需要用基地址+偏移的方式获取，基地址，首先点击下图的General 
 
下图红框的就是基地址 
 
偏移就是144A56400-140000000的结果，注意140000000和144A56400是十六进制数，如下图结果，4A56400，然后就找到了GName这个全局变量的地址

## 7. 7.UE-游戏逆向-绕过游戏的反调试

- URL: https://jisuanjiwang.blog.csdn.net/article/details/152132682
- Description: æç« æµè§éè¯»2.1kæ¬¡ï¼ç¹èµ39æ¬¡ï¼æ¶è20æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_è°æææ¸¸æçéåè°è¯å¨dhs

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：6.UE-游戏逆向-查找游戏中的GName，查找GName地址 
什么是反调试，就是不管使用CE还是spy++还是OD还是xdbg只要打开它就会被检测到，检测到会把这些调试软件（CE、spy++、OD、x32dbg、x64dbg）给关闭或游戏退出等操作，也就是说调试软件根本就打不开，本次写的是使用检测窗口（窗口类名、窗口标题）的手段来实现反调试的情况 
首先ue的游戏运行后会有下图红框的进程，SC-Plugin for UE4，它就是用来检测调试软件的 
 
如果使用任务管理器的结束任务按钮，关闭进程，它还是会自动运行 
 
怎么办？首先使用ida反编译游戏的exe文件，如下图ida反编译完成后 
 
然后ida里有一个导入表，下图的Imports就是导入表窗口 
 
然后按CTRL+F，然后输入FindW，就可以出现下图蓝框里的内容，下图蓝框里的FIndWindow开头的函数就是用来查找窗口的 
 
然后双击上图蓝框里的FIndWindowA进入下图位置，然后鼠标左键双击下图红框位置 
 
然后就进入了调用FIndWindowA函数的位置 
 
按下空格键，就能把上图的样子变成下图的样子，下图的样子比较好看 
 
如下图红框它们都是窗口的类名，也就是在这里进行的调试器检测 
 
然后按下F5，通过伪C++代码查看，通过下图可以看得出来通过GetProcAddress函数获取IsDebuggerPresent函数地址，然后调用IsDebuggerPresent函数从而得到当前是否有被调试，如果有被调试就退出，如果没有调试就调用OpenFileMappingW和FindWindowA检测调试器，所以说下图红框的函数，也就是叫sub_1408B4A60的函数是用来做反调试的，如果想过反调试就把sub_1408B4A60函数第一行写一句retn，retn的意思只要运行了retn就说明当前函数执行完了，然后返回 
 
代码说明

```text
// 函数：sub_1408B4A60
// 参数：a1（一个内存地址，可能是某个对象的指针）
// 返回值：HWND（窗口句柄，即窗口的唯一标识）
HWND __fastcall sub_1408B4A60(__int64 a1)
{
  HWND result; // 用于存储最终返回的窗口句柄
  HMODULE Library; // 用于加载的系统库（如kernel32.dll）
  BOOL (__stdcall *IsDebuggerPresent)(); // 指向"检查是否有调试器"的函数

// 第一步：尝试获取窗口句柄（两种方式）
  // 1. 先检查a1+48地址处的变量是否有效，或调用sub_14106D010()获取窗口句柄
  // 2. 如果失败，调用sub_1408BF9D0(a1)作为备用方案获取窗口句柄
  if ( !*(_QWORD *)(a1 + 48) || (result = (HWND)sub_14106D010(), !(_BYTE)result) )
    result = (HWND)sub_1408BF9D0(a1);

// 第二步：反调试检测（仅当a1+109地址处的标志为0时执行）
  if ( !*(_BYTE *)(a1 + 109) )
  {
    // 加载系统库kernel32.dll（包含基础系统函数）
    Library = LoadLibraryExW(L"kernel32.dll", 0, 0);
    // 从kernel32.dll中获取"IsDebuggerPresent"函数的地址
    // 这个函数的作用是：检查当前程序是否正在被调试器（如Visual Studio调试器）调试
    IsDebuggerPresent = (BOOL (__stdcall *)())GetProcAddress(Library, "IsDebuggerPresent");

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：6.UE-游戏逆向-查找游戏中的GName，查找GName地址 
什么是反调试，就是不管使用CE还是spy++还是OD还是xdbg只要打开它就会被检测到，检测到会把这些调试软件（CE、spy++、OD、x32dbg、x64dbg）给关闭或游戏退出等操作，也就是说调试软件根本就打不开，本次写的是使用检测窗口（窗口类名、窗口标题）的手段来实现反调试的情况 
首先ue的游戏运行后会有下图红框的进程，SC-Plugin for UE4，它就是用来检测调试软件的 
 
如果使用任务管理器的结束任务按钮，关闭进程，它还是会自动运行 
 
怎么办？首先使用ida反编译游戏的exe文件，如下图ida反编译完成后 
 
然后ida里有一个导入表，下图的Imports就是导入表窗口 
 
然后按CTRL+F，然后输入FindW，就可以出现下图蓝框里的内容，下图蓝框里的FIndWindow开头的函数就是用来查找窗口的 
 
然后双击上图蓝框里的FIndWindowA进入下图位置，然后鼠标左键双击下图红框位置 
 
然后就进入了调用FIndWindowA函数的位置 
 
按下空格键，就能把上图的样子变成下图的样子，下图的样子比较好看 
 
如下图红框它们都是窗口的类名，也就是在这里进行的调试器检测 
 
然后按下F5，通过伪C++代码查看，通过下图可以看得出来通过GetProcAddress函数获取IsDebuggerPresent函数地址，然后调用IsDebuggerPresent函数从而得到当前是否有被调试，如果有被调试就退出，如果没有调试就调用OpenFileMappingW和FindWindowA检测调试器，所以说下图红框的函数，也就是叫sub_1408B4A60的函数是用来做反调试的，如果想过反调试就把sub_1408B4A60函数第一行写一句retn，retn的意思只要运行了retn就说明当前函数执行完了，然后返回 
 
代码说明 

```text
// 函数：sub_1408B4A60
// 参数：a1（一个内存地址，可能是某个对象的指针）
// 返回值：HWND（窗口句柄，即窗口的唯一标识）
HWND __fastcall sub_1408B4A60(__int64 a1)
{
  HWND result; // 用于存储最终返回的窗口句柄
  HMODULE Library; // 用于加载的系统库（如kernel32.dll）
  BOOL (__stdcall *IsDebuggerPresent)(); // 指向"检查是否有调试器"的函数

  // 第一步：尝试获取窗口句柄（两种方式）
  // 1. 先检查a1+48地址处的变量是否有效，或调用sub_14106D010()获取窗口句柄
  // 2. 如果失败，调用sub_1408BF9D0(a1)作为备用方案获取窗口句柄
  if ( !*(_QWORD *)(a1 + 48) || (result = (HWND)sub_14106D010(), !(_BYTE)result) )
    result = (HWND)sub_1408BF9D0(a1);

  // 第二步：反调试检测（仅当a1+109地址处的标志为0时执行）
  if ( !*(_BYTE *)(a1 + 109) )
  {
    // 加载系统库kernel32.dll（包含基础系统函数）
    Library = LoadLibraryExW(L"kernel32.dll", 0, 0);
    // 从kernel32.dll中获取"IsDebuggerPresent"函数的地址
    // 这个函数的作用是：检查当前程序是否正在被调试器（如Visual Studio调试器）调试
    IsDebuggerPresent = (BOOL (__stdcall *)())GetProcAddress(Library, "IsDebuggerPresent");

    // 如果成功获取到IsDebuggerPresent函数，且调用后发现有调试器
    if ( IsDebuggerPresent && ((__int64 (*)(void))IsDebuggerPresent)() )
    {
      FreeLibrary(Library); // 释放加载的kernel32.dll
      return (HWND)sub_140F432C0(0); // 触发反制（可能是退出程序、报错等）
    }
    else
    {
      FreeLibrary(Library); // 没有调试器，释放库

      // 检查是否存在名为"CEHYPERSCANSETTINGS"的文件映射（Cheat Engine的特征）
      if ( OpenFileMappingW(6u, 0, L"CEHYPERSCANSETTINGS") )
        return (HWND)sub_140F432C0(0); // 检测到Cheat Engine，触发反制

      // 检查是否存在WinDbg调试器窗口（类名为"WinDbgFrameClass"）
      if ( FindWindowA("WinDbgFrameClass", 0) )
        return (HWND)sub_140F432C0(0); // 检测到WinDbg，触发反制
      
      // 重复检查WinDbg窗口（可能是冗余逻辑或特定场景适配）
      if ( FindWindowA("WinDbgFrameClass", 0) )
        return (HWND)sub_140F432C0(0);

      // 检查是否存在OllyDbg调试器窗口（类名为"OLLYDBG"）
      if ( FindWindowA("OLLYDBG", 0) )
        return (HWND)sub_140F432C0(0); // 检测到OllyDbg，触发反制

      // 检查是否存在类名为"Window"的可疑窗口（可能是其他调试/作弊工具）
      result = FindWindowA("Window", 0);
      if ( result )
        return (HWND)sub_140F432C0(0); // 检测到可疑窗口，触发反制
    }
  }

  // 如果没检测到调试器，返回之前获取的窗口句柄
  return result;
}

```
 
然后点击下图红框的IDA VIew-A，然后鼠标左键单击sub_1408B4A60头部 
 
然后选择下图中的Change byte 
 
然后把下图红框的内容替换成c3，c3的就代表了汇编代码retn，也就是说retn这个汇编代码的硬编码是c3 
 
改完之后如下图红框，第一行就变成了retn，游戏是x64的不需要关心堆栈平衡 
 
改完之后点击下图中的 Apply patches to input file进行保存 
 
什么都不需要改直接点击ok，注意如果游戏在运行它会保存失败 
 
然后再次打开游戏，然后再次找到 SC-Plugin for UE4进行，然后选中它，然后点击结束任务，就会发现SC-Plugin for UE4不会再次运行了，然后就可以打开调试器了，spy++也能打开获取游戏的窗口类名了 
 
如下图石头spy++获取类名和打开ce

## 8. 8.UE-游戏逆向-代码实现GetName算法（一）

- URL: https://jisuanjiwang.blog.csdn.net/article/details/152228719
- Description: æç« æµè§éè¯»1.4kæ¬¡ï¼ç¹èµ12æ¬¡ï¼æ¶è9æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ èå¹» ue UnrealEngine_ue5éååç±»idåç±»å

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：7.UE-游戏逆向-绕过游戏的反调试 
代码的说明放在了最后，下方的过程主要是介绍代码写法的来源 
首先打开vs2022创建一个新项目 
 
然后选择控制台应用 
 
然后设置保存位置和项目名称，然后点击创建 
 
编写的代码，下图红框是复制的UE源码中通过GName找字符串的算法，然后就要去UE源码中把FNameEntry和Blocks复制出来，不需要全部复制，只需要一部分就可以 
 
首先是FNameEntry，按着CTRL鼠标左键单击下图红框 
 
只需要复制下图红框的部分 
 
复制过去后，补上下图红框的大括号 
 
然后把FNameEntry里多余的代码删了 
 
然后再找下图红框的代码 
 
还是按着CTRL鼠标左键单击下图红框 
 
把下图红框的代码复制过去 
 
复制过来后，改一下，最终的代码如下图红框 
 
然后FNameEntry里剩下的代码修改，如下图红框 
 
然后FNameEntryHeader里还可以再改一下，如下图红框 
 
然后还剩下，下图红框的Blocks，Blocks它在GName里面 
 
然后再来回忆一下GName，首先Blocks是在FNameEntryAllocator里面 
 
然后FNameEntryAllocator在FNamePool里面，然后FNamePool里面通过调用FNameEntryAllocator里的Resolve函数得到取字符串的算法*reinterpret_cast<FNameEntry*>(Blocks[Handle.Block] + Stride * Handle.Offset); 
 
所以现在得到的GName是FNamePool结构，然后FNameEntryAllocator在FNamePool第一个位置让，然后Blocks在FNameEntryAllocator的8+4+4位置，8+4+4的结果是16，16的十六进制是10，如下图改好的代码 
 
然后Blocks是uint8*类型，所以还要改一下 
 
最终的代码 
 
导致就把代码复制完了，然后完整的代码，现在的代码没法运行，下一节继续完善

```text
// ShiXianGetNameSuanFa.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
// 简单说：这个程序是用来从游戏里读取"名字"的，通过游戏里的GName系统，根据ID找到对应的字符串

// 引入需要的工具库
#include <iostream>   // 用于输入输出（比如打印文字到屏幕）
#include <string>     // 用于处理字符串（比如存储读取到的名字）
#include <windows.h>  // 用于调用Windows系统功能（比如读取其他程序的内存）

using namespace std;  // 简化代码，不用每次写"std::"

// 定义一个结构体，用来存储字符串的"元信息"（类似标签，记录字符串的基本属性）
struct FNameEntryHeader
{
    // 位域：把16位的空间分成几个小部分（节省内存）
    uint16_t bIsWide : 1;        // 占1位：标识字符串是宽字符（1）还是普通字符（0）
                                 // 宽字符（wchar_t）能存中文，普通字符（char）只能存英文/数字

uint16_t LowercaseProbeHash : 5;  // 占5位：小写哈希值（用于快速比较字符串是否相同）
    uint16_t Len : 10;               // 占10位：字符串的长度（有多少个字符，比如"abc"长度是3）
};

// 定义一个结构体，用来存储字符串的实际数据（包含元信息和字符内容）
struct FNameEntry
{
    FNameEntryHeader Header;  // 上面定义的元信息（长度、是否宽字符等）

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：7.UE-游戏逆向-绕过游戏的反调试 
代码的说明放在了最后，下方的过程主要是介绍代码写法的来源 
首先打开vs2022创建一个新项目 
 
然后选择控制台应用 
 
然后设置保存位置和项目名称，然后点击创建 
 
编写的代码，下图红框是复制的UE源码中通过GName找字符串的算法，然后就要去UE源码中把FNameEntry和Blocks复制出来，不需要全部复制，只需要一部分就可以 
 
首先是FNameEntry，按着CTRL鼠标左键单击下图红框 
 
只需要复制下图红框的部分 
 
复制过去后，补上下图红框的大括号 
 
然后把FNameEntry里多余的代码删了 
 
然后再找下图红框的代码 
 
还是按着CTRL鼠标左键单击下图红框 
 
把下图红框的代码复制过去 
 
复制过来后，改一下，最终的代码如下图红框 
 
然后FNameEntry里剩下的代码修改，如下图红框 
 
然后FNameEntryHeader里还可以再改一下，如下图红框 
 
然后还剩下，下图红框的Blocks，Blocks它在GName里面 
 
然后再来回忆一下GName，首先Blocks是在FNameEntryAllocator里面 
 
然后FNameEntryAllocator在FNamePool里面，然后FNamePool里面通过调用FNameEntryAllocator里的Resolve函数得到取字符串的算法*reinterpret_cast<FNameEntry*>(Blocks[Handle.Block] + Stride * Handle.Offset); 
 
所以现在得到的GName是FNamePool结构，然后FNameEntryAllocator在FNamePool第一个位置让，然后Blocks在FNameEntryAllocator的8+4+4位置，8+4+4的结果是16，16的十六进制是10，如下图改好的代码 
 
然后Blocks是uint8*类型，所以还要改一下 
 
最终的代码 
 
导致就把代码复制完了，然后完整的代码，现在的代码没法运行，下一节继续完善 

```text
// ShiXianGetNameSuanFa.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
// 简单说：这个程序是用来从游戏里读取"名字"的，通过游戏里的GName系统，根据ID找到对应的字符串

// 引入需要的工具库
#include <iostream>   // 用于输入输出（比如打印文字到屏幕）
#include <string>     // 用于处理字符串（比如存储读取到的名字）
#include <windows.h>  // 用于调用Windows系统功能（比如读取其他程序的内存）

using namespace std;  // 简化代码，不用每次写"std::"

// 定义一个结构体，用来存储字符串的"元信息"（类似标签，记录字符串的基本属性）
struct FNameEntryHeader
{
    // 位域：把16位的空间分成几个小部分（节省内存）
    uint16_t bIsWide : 1;        // 占1位：标识字符串是宽字符（1）还是普通字符（0）
                                 // 宽字符（wchar_t）能存中文，普通字符（char）只能存英文/数字

    uint16_t LowercaseProbeHash : 5;  // 占5位：小写哈希值（用于快速比较字符串是否相同）
    uint16_t Len : 10;               // 占10位：字符串的长度（有多少个字符，比如"abc"长度是3）
};

// 定义一个结构体，用来存储字符串的实际数据（包含元信息和字符内容）
struct FNameEntry
{
    FNameEntryHeader Header;  // 上面定义的元信息（长度、是否宽字符等）

    // 联合体：两种字符存储方式共用一块内存（节省空间，用不到的不占额外内存）
    union
    {
        char AnsiName[1024];    // 普通字符数组（存英文/数字等，每个字符占1字节，最多1024个）
        wchar_t WideName[1024]; // 宽字符数组（存中文等，每个字符占2字节，最多1024个）
    };
};

// 游戏中"全局名字池"（GName）的地址（这是通过工具逆向游戏找到的，不同游戏/版本不一样）
// 简单说：GName就像游戏里的"名字字典"，所有用到的名字都存在这里，每个名字有唯一ID
uint8_t* GName = (uint8_t*)(0x4A56400 + 0x10);  // 0x4A56400是基地址，加0x10是实际存储地址

// 函数：读取游戏进程中某个内存地址的数据（获取GName里的块地址）
// 参数：a是要读取的内存地址
// 返回：读取到的地址（指向GName中的一块数据）
uint8_t* MyReadProessMemory(uint8_t* a) {
    // 1. 找到游戏窗口（UnrealWindow是UE引擎游戏的窗口类名，大部分UE游戏都用这个）
    HWND nhwnd = FindWindowA("UnrealWindow", 0);  // 0表示不指定窗口标题，只按类名找

    // 2. 获取游戏进程的ID（每个运行的程序都有唯一ID，类似身份证号）
    DWORD pid = 0;  // 用来存进程ID
    GetWindowThreadProcessId(nhwnd, &pid);  // 通过窗口句柄获取进程ID，存到pid里

    // 3. 打开游戏进程，获取访问权限（类似拿到进入房间的钥匙）
    // PROCESS_ALL_ACCESS表示请求所有权限（实际只需要读内存权限即可）
    HANDLE nhandle = OpenProcess(PROCESS_ALL_ACCESS, 0, pid);

    // 4. 读取目标地址的内存（从游戏里把数据读出来）
    uint8_t buf;  // 用来存读取到的数据（注意：这里原代码有问题，应该用8字节变量存地址）
    // 读取a地址处的8个字节（因为地址是8字节），存到buf里
    ReadProcessMemory(nhandle, a, &buf, 8, NULL);

    return (uint8_t*)buf;  // 返回读取到的地址（实际是被截断的，原代码这里有bug）
}

// 函数：读取游戏进程中某个FNameEntry结构体的数据（包含字符串实际内容）
// 参数：a是FNameEntry在游戏内存中的地址
// 返回：读取到的FNameEntry结构体（包含元信息和字符）
FNameEntry MyReadProessMemoryFNameEntry(FNameEntry* a) {
    // 步骤和上面类似：找窗口→拿进程ID→开进程权限
    HWND nhwnd = FindWindowA("UnrealWindow", 0);
    DWORD pid = 0;
    GetWindowThreadProcessId(nhwnd, &pid);
    HANDLE nhandle = OpenProcess(PROCESS_ALL_ACCESS, 0, pid);

    // 读取FNameEntry结构体（大小是sizeof(FNameEntry)）
    FNameEntry buf;  // 用来存读取到的结构体
    ReadProcessMemory(nhandle, a, &buf, sizeof(FNameEntry), NULL);

    return buf;  // 返回读取到的结构体
}

// 函数：根据ID获取对应的名字（核心功能）
// 参数：id是名字在GName中的唯一编号（比如0、1、2...）
// 返回：对应的字符串（比如ID=0可能对应"None"）
string GetName(int id) {
    // 1. 计算GName中"块"的地址（GName把名字分成很多块存储，类似字典分章节）
    // id >> 16：把ID的高16位作为块索引（找到是哪一"章"）
    // 每个块的地址占8字节，所以乘以8找到在GName中的位置
    uint8_t* a = MyReadProessMemory(GName + (id >> 16) * 8);

    // 2. 计算块内的偏移（在这一"章"里找具体位置）
    // id & 65535：取ID的低16位（65535是16位全1，相当于取后16位）
    // 乘以2作为偏移量（原代码逻辑，实际可能需要根据结构体大小计算）
    uint8_t* b = (uint8_t*)(2 * (id & 65535));

    // 3. 找到具体的FNameEntry地址，读取数据
    // a是块地址，加b的偏移就是具体条目地址，读取这个条目的数据
    FNameEntry  info = MyReadProessMemoryFNameEntry((FNameEntry*)(DWORD64)a + b);

    // 4. 从FNameEntry中提取字符串（用元信息里的长度Len作为字符串长度）
    return string(info.AnsiName, info.Header.Len);
}

// 程序入口（从这里开始执行）
int main()
{
    // 调用GetName函数获取ID=0的名字，并打印到屏幕
    printf("GetName=%s", GetName(0).c_str());
}

```

## 9. 9.UE-游戏逆向-代码实现GetName算法（二）-使用CE手动找GName字符串

- URL: https://jisuanjiwang.blog.csdn.net/article/details/152280157
- Description: æç« æµè§éè¯»1.9kæ¬¡ï¼ç¹èµ27æ¬¡ï¼æ¶è13æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ èå¹»å¼æ UE UnrealEngine_ue4éæä¹å¿«éç¨ceæ¾gnameå°å

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：8.UE-游戏逆向-代码实现GetName算法（一） 
基于上一个内容里的代码修改下图红框的代码 
 
然后再改下图红框，修改完就可以用了 
 
用之前，需要找一下游戏的地址，通过得到游戏的地址，然后加GName的偏移来得到GName，找游戏的基址首先打开CE，然后点击下图红框 
 
然后选择游戏，然后点击打开 
 
然后就附加到游戏了 
 
然后找游戏的exe文件，首先打开任务管理器，鼠标右击游戏的进程，选择打开文件所在的位置 
 
复制一下游戏的名字 
 
然后点击下图红框的按钮 
 
然后把游戏名字复制到下图红框，然后选择8字节 
 
下图红框就是游戏的地址了 
 
然后把游戏的地址写到代码里，如下图红框的位置 
 
然后点击运行 
 
如下图红框，就可以看到游戏中的字符串了 
 
然后游戏中的字符串，如下图红框已知的有702个，接下来把它们全部打印出来 
 
如下图红框都可以看到，但打印的内容有点问题，这可能我们给的id不怎么对，这个不要紧 
 
然后接下来使用CE手动找字符串，首先复制下图红框，找到FNamePool类 
 
然后点击下图红框 
 
然后把复制的FNamePool地址放到下图红框，然后点击确定 
 
然后右击选择浏览相关内存区域 
 
然后就来到了它的内存 
 
然后鼠标右击选择8字节(HEX)，也就是以8字节十六进制的方式显示内存 
 
然后打开UE的源码对比着看，下图红框的内存数据就是下图蓝框变量里的成员变量，也就是FNameEntryAllocator里面的内容 
 
然后就进入FNameEntryAllocator里面再对比，如下图变量对应的内存数据，可以看出下图红框的就是Blocks，也就是字符串存放的变量 
 
然后知道Blocks的位置后，就带入id手动去找一下，这里id的值带入的是0也就是None的位置，0右移16还是0，所以就找Blocks位置0的地方，也就是下图红框的位置 
 
然后鼠标右击选择前进 
 
然后如下图红框就可以看到我们认识的字符串了，也就是得到了一个FNameEntry 
 
但是这个字符串里有..这样的东西，接下来写它是怎样把这些..给过滤掉的 
 
然后接下来就要分析FNameEntry的结构，如下图红框结构说明，这里可能感觉对不上号，等会看到内存里的数据就能明白了 
 
然后如下图红框，把字符串的地址，以2字节的方式读取 
 
然后鼠标右击以十六进制显示 
 
也就是对应下图红框的三个变量，这三个里面我们用Len，它是字符串的长度 
 
想知道Len的数据就是用11E右移6位，也就是把bIsWide和LowercaseProbeHash的数据移除，11E右移6的结果是4，也就是说字符串的长度（文字的长度是4字节） 
 
然后来到CE，如下图红框0x241E8D70000+2的意思是，bIsWide和LowercaseProbeHash和Len是2字节，这里+2就是把它们三个去掉，去掉之后才是字符串 
 
也就得到了None，移除了..的数据，也就是下图红框的AnsiName和WideName变量，这俩变量都指向0x241E8D70000+2这个内存地址，具体用AnsiName还是WideName取决于字符串的编码 
 
完整代码

```text
// ShiXianGetNameSuanFa.cpp : 程序的主文件，程序从这里开始并结束运行
// 功能：从UE引擎游戏中读取"全局名字池"（GName）里的字符串，按ID从0到701依次打印

#include <iostream>   // 用于屏幕打印文字
#include <string>     // 用于处理字符串
#include <windows.h>  // 用于调用Windows系统功能（如读取其他程序内存）

using namespace std;  // 简化代码，不用每次写"std::"

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：8.UE-游戏逆向-代码实现GetName算法（一） 
基于上一个内容里的代码修改下图红框的代码 
 
然后再改下图红框，修改完就可以用了 
 
用之前，需要找一下游戏的地址，通过得到游戏的地址，然后加GName的偏移来得到GName，找游戏的基址首先打开CE，然后点击下图红框 
 
然后选择游戏，然后点击打开 
 
然后就附加到游戏了 
 
然后找游戏的exe文件，首先打开任务管理器，鼠标右击游戏的进程，选择打开文件所在的位置 
 
复制一下游戏的名字 
 
然后点击下图红框的按钮 
 
然后把游戏名字复制到下图红框，然后选择8字节 
 
下图红框就是游戏的地址了 
 
然后把游戏的地址写到代码里，如下图红框的位置 
 
然后点击运行 
 
如下图红框，就可以看到游戏中的字符串了 
 
然后游戏中的字符串，如下图红框已知的有702个，接下来把它们全部打印出来 
 
如下图红框都可以看到，但打印的内容有点问题，这可能我们给的id不怎么对，这个不要紧 
 
然后接下来使用CE手动找字符串，首先复制下图红框，找到FNamePool类 
 
然后点击下图红框 
 
然后把复制的FNamePool地址放到下图红框，然后点击确定 
 
然后右击选择浏览相关内存区域 
 
然后就来到了它的内存 
 
然后鼠标右击选择8字节(HEX)，也就是以8字节十六进制的方式显示内存 
 
然后打开UE的源码对比着看，下图红框的内存数据就是下图蓝框变量里的成员变量，也就是FNameEntryAllocator里面的内容 
 
然后就进入FNameEntryAllocator里面再对比，如下图变量对应的内存数据，可以看出下图红框的就是Blocks，也就是字符串存放的变量 
 
然后知道Blocks的位置后，就带入id手动去找一下，这里id的值带入的是0也就是None的位置，0右移16还是0，所以就找Blocks位置0的地方，也就是下图红框的位置 
 
然后鼠标右击选择前进 
 
然后如下图红框就可以看到我们认识的字符串了，也就是得到了一个FNameEntry 
 
但是这个字符串里有..这样的东西，接下来写它是怎样把这些..给过滤掉的 
 
然后接下来就要分析FNameEntry的结构，如下图红框结构说明，这里可能感觉对不上号，等会看到内存里的数据就能明白了 
 
然后如下图红框，把字符串的地址，以2字节的方式读取 
 
然后鼠标右击以十六进制显示 
 
也就是对应下图红框的三个变量，这三个里面我们用Len，它是字符串的长度 
 
想知道Len的数据就是用11E右移6位，也就是把bIsWide和LowercaseProbeHash的数据移除，11E右移6的结果是4，也就是说字符串的长度（文字的长度是4字节） 
 
然后来到CE，如下图红框0x241E8D70000+2的意思是，bIsWide和LowercaseProbeHash和Len是2字节，这里+2就是把它们三个去掉，去掉之后才是字符串 
 
也就得到了None，移除了..的数据，也就是下图红框的AnsiName和WideName变量，这俩变量都指向0x241E8D70000+2这个内存地址，具体用AnsiName还是WideName取决于字符串的编码 
 
完整代码 

```text
// ShiXianGetNameSuanFa.cpp : 程序的主文件，程序从这里开始并结束运行
// 功能：从UE引擎游戏中读取"全局名字池"（GName）里的字符串，按ID从0到701依次打印

#include <iostream>   // 用于屏幕打印文字
#include <string>     // 用于处理字符串
#include <windows.h>  // 用于调用Windows系统功能（如读取其他程序内存）

using namespace std;  // 简化代码，不用每次写"std::"

// 字符串头部信息结构体（存储字符串的基本属性）
struct FNameEntryHeader
{
    // 位域：将2字节（16位）分成多个小部分，节省内存
    uint16_t bIsWide : 1;       // 1位：是否为宽字符（1=是，可存中文；0=否，仅存英文）
    uint16_t LowercaseProbeHash : 5;  // 5位：小写哈希值（用于快速比较字符串）
    uint16_t Len : 10;               // 10位：字符串长度（最多1023个字符）
};

// 字符串数据结构体（包含头部信息和实际字符）
struct FNameEntry
{
    FNameEntryHeader Header;  // 字符串的头部信息（长度、是否宽字符等）

    // 联合体：两种字符存储方式共用一块内存（节省空间）
    union
    {
        char AnsiName[1024];    // 普通字符数组（存英文/数字，1字节/字符）
        wchar_t WideName[1024]; // 宽字符数组（存中文等，2字节/字符）
    };
};

// 游戏中"全局名字池"（GName）的地址
// GName相当于游戏的"名字字典"，所有用到的名字都存在这里，每个名字有唯一ID
// 地址说明：0x7FF76F580000（游戏程序基地址） + 0x4A56400（GName偏移） + 0x10（实际存储位置）
// 注意：这个地址是逆向游戏得到的，换游戏或更新后会变化
uint8_t* GName = (uint8_t*)(0x7FF76F580000 + 0x4A56400 + 0x10);

// 从游戏进程中读取指定地址的内存（获取GName中的"块地址"）
// 参数：a = 要读取的游戏内存地址
// 返回：读取到的"块地址"（GName中存储名字的一个区块起始位置）
uint8_t* MyReadProessMemory(uint8_t* a) {
    // 1. 找到游戏窗口（UE引擎游戏的窗口类名通常是"UnrealWindow"）
    HWND nhwnd = FindWindowA("UnrealWindow", 0);  // 0 = 不限制窗口标题

    // 2. 获取游戏进程ID（每个运行的程序都有唯一ID，类似身份证号）
    DWORD pid = 0;
    GetWindowThreadProcessId(nhwnd, &pid);  // 通过窗口句柄获取进程ID

    // 3. 打开游戏进程，获取读取内存的权限（类似拿到访问游戏内存的钥匙）
    HANDLE nhandle = OpenProcess(PROCESS_ALL_ACCESS, 0, pid);

    // 4. 读取目标地址的8字节数据（64位系统中地址占8字节）
    uint8_t* buf;  // 存储读取到的地址
    ReadProcessMemory(nhandle, a, &buf, 8, NULL);

    return (uint8_t*)buf;  // 返回读取到的"块地址"
}

// 从游戏进程中读取指定地址的FNameEntry结构体（包含字符串实际内容）
// 参数：a = FNameEntry在游戏内存中的地址
// 返回：读取到的FNameEntry结构体（包含字符串数据）
FNameEntry MyReadProessMemoryFNameEntry(FNameEntry* a) {
    // 1. 找到游戏窗口并获取进程ID（和上面步骤相同）
    HWND nhwnd = FindWindowA("UnrealWindow", 0);
    DWORD pid = 0;
    GetWindowThreadProcessId(nhwnd, &pid);

    // 2. 打开游戏进程
    HANDLE nhandle = OpenProcess(PROCESS_ALL_ACCESS, 0, pid);

    // 3. 读取整个FNameEntry结构体（包含头部和字符数据）
    FNameEntry buf;  // 存储读取到的结构体
    ReadProcessMemory(nhandle, a, &buf, sizeof(FNameEntry), NULL);

    return buf;  // 返回读取到的字符串数据
}

// 根据ID获取对应的名字（核心函数）
// 参数：id = 名字在GName中的唯一编号（0、1、2...）
// 返回：id对应的字符串（如"Player"、"Item"等）
string GetName(int id) {
    // 1. 计算GName中"块"的地址（GName按"块"存储名字，类似字典分章节）
    // id >> 16 = 取ID的高16位作为"块索引"（确定是哪一章）
    // 每个块的地址占8字节，所以乘以8定位到块在GName中的位置
    uint8_t* a = MyReadProessMemory(GName + (id >> 16) * 8);

    // 2. 计算块内偏移（确定是这一章的第几页）
    // id & 65535 = 取ID的低16位（65535 = 2^16 - 1，刚好取低16位）
    // 乘以2作为偏移量（原代码逻辑，实际应按结构体大小计算）
    uint8_t* b = (uint8_t*)(2 * (id & 65535));

    // 3. 计算具体字符串的地址并读取数据
    // a（块地址） + b（块内偏移） = 该ID对应的字符串数据地址
    FNameEntry info = MyReadProessMemoryFNameEntry((FNameEntry*)((DWORD64)a + b));

    // 4. 从结构体中提取字符串（按头部信息的长度截取）
    return string(info.AnsiName, info.Header.Len);
}

// 程序入口（从这里开始执行）
int main()
{
    // 循环读取ID从0到701的名字，并打印到屏幕
    for (int i = 0; i < 702; i++)
    {
        printf("GetName=%s\n", GetName(i).c_str());  // 打印格式：GetName=名字内容
    }
}
```

## 10. 10.UE-游戏逆向-查找UObject（UObject偏移和FUObjectArray）

- URL: https://jisuanjiwang.blog.csdn.net/article/details/152334297
- Description: æç« æµè§éè¯»2.8kæ¬¡ï¼ç¹èµ55æ¬¡ï¼æ¶è44æ¬¡ãèå¹»å¼æ UE UnrealEngine æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ _ueéå

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：9.UE-游戏逆向-代码实现GetName算法（二）-使用CE手动找GName字符串 
UObject是ue中的对象模型，就是用来表示游戏中各种实体、资源和组件，UObject是虚幻引擎中的基类，所有的实体和资源都是基于UObject来实现的，如果说是正向开发还有需要了解很多东西，逆向而言只需要知道UObject是一个对象（对象代表任何东西任何数据，很抽象），在UE4中万物都是对象。这一段话看不懂没关系，后面实际用的时候，通过它的用法和用了之后会有一个什么效果来理解就可以了 
查找UObject，首先要知道要找的东西是什么，要找的东西是GUObjectArray 
然后打开UE4的源码，搜索GUObjectArray，如下图选择在文件中查找 
 
然后输入GUObjectArray，然后点击查找全部 
 
然后这里就使用第一个作为入口，也就是鼠标左键双击下图红框 
 
然后按着CTRL鼠标左键单击下图红框 
 
然后就找到了GUObjectArray的变量，它是一个FUObjectArray的类型，我们要找的也就是FUObjectArray类型的首地址 
 
然后找FUObjectArray它的首地址，也就是要使用IDA工具，但是使用IDA工具需要一个字符串（之前通过字符串定位的GName），上图红框位置就没有字符串，所以还要找一下别的位置，使用下图红框位置的UObjectBase.cpp里面，它可以 
 
然后双击下图蓝框，就可以跳转到下图红框位置 
 
然后往上滑，可以看到下图红框有一个SCOPED_BOOT_TIMING("UObjectBaseInit");，这个字符串就可以使用IDA搜索到 
 
下图红框也是字符串，但是使用IDA搜不到，也就没法用 
 
然后打开ida，然后点击names 
 
然后按CTRL+F然后输入UObjectBaseIni，注意把最后一个t给删了，不然也还是搜索不到，如下图红框 
 
然后双击下图红框 
 
在names窗口里它显示的不全，双击之后它是全的，如下图红框 
 
然后再双击下图红框位置， 
 
双击完就跳转了使用字符串的代码里 
 
如下图的内容所示，和UE4源码做对比，它都可以对的上 
 
然后按F5让它生成伪代码 
 
下图红框的就是GUObjectArray 
 
下方这一段代码，是调用成员函数，是C++语言的写法，C++代码编译成汇编代码后，是AllocateObjectPool(GUObjectArray的地址,MaxUObjects, MaxObjectsNotConsideredByGC, bPreAllocateUObjectArray)这样的，所以说上图红框是GUObjectArray

```text
GUObjectArray.AllocateObjectPool(MaxUObjects, MaxObjectsNotConsideredByGC, bPreAllocateUObjectArray);

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：9.UE-游戏逆向-代码实现GetName算法（二）-使用CE手动找GName字符串 
UObject是ue中的对象模型，就是用来表示游戏中各种实体、资源和组件，UObject是虚幻引擎中的基类，所有的实体和资源都是基于UObject来实现的，如果说是正向开发还有需要了解很多东西，逆向而言只需要知道UObject是一个对象（对象代表任何东西任何数据，很抽象），在UE4中万物都是对象。这一段话看不懂没关系，后面实际用的时候，通过它的用法和用了之后会有一个什么效果来理解就可以了 
查找UObject，首先要知道要找的东西是什么，要找的东西是GUObjectArray 
然后打开UE4的源码，搜索GUObjectArray，如下图选择在文件中查找 
 
然后输入GUObjectArray，然后点击查找全部 
 
然后这里就使用第一个作为入口，也就是鼠标左键双击下图红框 
 
然后按着CTRL鼠标左键单击下图红框 
 
然后就找到了GUObjectArray的变量，它是一个FUObjectArray的类型，我们要找的也就是FUObjectArray类型的首地址 
 
然后找FUObjectArray它的首地址，也就是要使用IDA工具，但是使用IDA工具需要一个字符串（之前通过字符串定位的GName），上图红框位置就没有字符串，所以还要找一下别的位置，使用下图红框位置的UObjectBase.cpp里面，它可以 
 
然后双击下图蓝框，就可以跳转到下图红框位置 
 
然后往上滑，可以看到下图红框有一个SCOPED_BOOT_TIMING("UObjectBaseInit");，这个字符串就可以使用IDA搜索到 
 
下图红框也是字符串，但是使用IDA搜不到，也就没法用 
 
然后打开ida，然后点击names 
 
然后按CTRL+F然后输入UObjectBaseIni，注意把最后一个t给删了，不然也还是搜索不到，如下图红框 
 
然后双击下图红框 
 
在names窗口里它显示的不全，双击之后它是全的，如下图红框 
 
然后再双击下图红框位置， 
 
双击完就跳转了使用字符串的代码里 
 
如下图的内容所示，和UE4源码做对比，它都可以对的上 
 
然后按F5让它生成伪代码 
 
下图红框的就是GUObjectArray 
 
下方这一段代码，是调用成员函数，是C++语言的写法，C++代码编译成汇编代码后，是AllocateObjectPool(GUObjectArray的地址,MaxUObjects, MaxObjectsNotConsideredByGC, bPreAllocateUObjectArray)这样的，所以说上图红框是GUObjectArray 

```text
GUObjectArray.AllocateObjectPool(MaxUObjects, MaxObjectsNotConsideredByGC, bPreAllocateUObjectArray);

```
 
然后GUObjectArray的偏移0x4A92740，到这就可以定位到GUObjectArray了，然后接下来找UObject，然后通过查看FUObjectArray这个类型里面都有什么来找UObject，按着CTRL鼠标左键单击下图红框，进入FUObjectArray类型 
 
进入之后往下滑，找它的成员变量，也就是下图红框 
 
它里面有一个TUObjectArray，然后安装CTRL鼠标左键单击下图红框，进入TUObjectArray 
 
然后TUObjectArray是一个FChunkedFixedUObjectArray类型，然后CTRL鼠标左键单击下图红框进入FChunkedFixedUObjectArray 
 
FChunkedFixedUObjectArray 
 
然后还需要看 FUObjectItem，也就是下图红框的类型，按着CTRL鼠标左键单击下图红框 
 
如下图FUObjectItem， 
 
然后再看UObjectBase，还是按着CTRL鼠标左键单击下图红框 
 
UObjectBase，这个UObjectBase是万物之源，UObject是基于它生成的，然后FUObjectArray是一个UObject数组，可以说它实际上是UObjectBase 
 
知道上方的内容后，接下来就要下载一些东西了，下载的目的是方便后续去找数据，找偏移，找函数的地址，下载搞明白就能对UE的结构有一个深入的了解 
总结： 
 
 GUObjectArray的偏移0x4A92740 
 FUObjectArray继承图

## 11. 11.UE-游戏逆向-内存中的FUObjectArray（深入理解内存数据）

- URL: https://jisuanjiwang.blog.csdn.net/article/details/152401883
- Description: æç« æµè§éè¯»1kæ¬¡ï¼ç¹èµ25æ¬¡ï¼æ¶è11æ¬¡ãèå¹» UnrealEngine4 æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_fchunkedfixeduobjectarray

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：10.UE-游戏逆向-查找UObject（UObject偏移和FUObjectArray） 
首先打开游戏，然后使用任务管理器把SC-Plugin for UE4进程关闭掉（如果关不掉说明检测没有处理，去看之前的内容进行处理） 
 
然后使用ce附加，然后点击下图红框 手动添加地址 
 
游戏exe的文件名+上一个内容中找到的FUObjectArray偏移，也就是0x4A92740，然后点击确定 
 
然后选择浏览相关内存区域 
 
然后选择以8字节十六进制显示 
 
然后对比源码，只要是看绿框的TUObjectArray类型 
 
然后接下来对比TUObjectArray类型，然后看FUObjectItem类型 
 
FUObjectItem** 这样的写法说明内存地址里存放的是一个内存地址，然后内存地址里放的还是内存地址，最终指向一个以FUObjectItem结构存放的内存数据，鼠标单击下图红框，然后按空格键 
 
然后就进入了1DA8F737B40这个内存地址了，然后上方说，内存地址里放的还是内存地址 
 
然后单击下图红框，然后再按空格键进入1DA903B0008内存地址 
 
然后下图就是以FUObjectItem结构存放的数据了 
 
然后对比源码，到这可以应该是可以更深入的理解数据结构这个概念了 
 
然后鼠标右击选择后退，后退到TUObjectArray里也就是FChunkedFixedUObjectArray里 
 
下图红框的代码 
 
代码说明，里面的元素概念指的是FUObjectItem，然后FUObjectItem存放的是UObject，然后UObject指的是角色、武器、道具、组件等游戏中的东西，然后块的概念是可以存放多少个FUObjectItem

```text
/** 主表：指向多个"块"的总目录（二级指针数组）
 *  关系：
 *  - 每个"块"（Chunk）是一个数组，里面装着多个"元素"（FUObjectItem）
 *  - 主表（Objects）就像"仓库货架清单"，清单上的每个条目都指向一个货架（块）
 *  - 通过主表能快速找到所有货架，再从货架上找到具体的元素
 */
FUObjectItem** Objects;

/** 预分配的连续内存块：所有元素集中存放的"超级货架"
 *  关系：
 *  - 这是一块连续的内存，里面直接按顺序放着多个"元素"（FUObjectItem）
 *  - 和上面的"多块分散存储"不同，这里是"一块集中存储"，访问速度更快
 *  - 相当于把所有标签（元素）都整齐地放在一个超大盒子里，而不是多个小盒子
 */
FUObjectItem* PreAllocatedObjects;

/** 最大元素数量：系统能管理的最多"元素"总数
 *  关系：
 *  - "元素"（Element）就是单个FUObjectItem，每个对应一个游戏对象（UObject）
 *  - 这个值是上限，比如"最多能有10000个标签"，不管这些标签放在多少个块里
 */
int32 MaxElements;

/** 当前元素数量：现在实际存在的"元素"总数
 *  关系：
 *  - 等于所有块里的元素数量相加（比如3个块各有100、200、300个元素，总数就是600）
 *  - 每个元素对应一个真实的游戏对象，这个数越多，说明当前加载的对象越多
 */
int32 NumElements;

/** 最大块数量：主表（Objects）能容纳的最多"块"总数
 *  关系：
 *  - "块"（Chunk）是装元素的容器（数组），比如"最多能有10个盒子"
 *  - 超过这个数就需要扩容主表，否则无法新增块
 */
int32 MaxChunks;

/** 当前块数量：现在实际存在的"块"总数
 *  关系：
 *  - 每个块里都装着若干元素（比如当前有5个盒子，每个盒子里装着不同数量的标签）
 *  - 当元素数量增加，现有块装不下时，会新增块（这个数会增加）
 */
int32 NumChunks;

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：10.UE-游戏逆向-查找UObject（UObject偏移和FUObjectArray） 
首先打开游戏，然后使用任务管理器把SC-Plugin for UE4进程关闭掉（如果关不掉说明检测没有处理，去看之前的内容进行处理） 
 
然后使用ce附加，然后点击下图红框 手动添加地址 
 
游戏exe的文件名+上一个内容中找到的FUObjectArray偏移，也就是0x4A92740，然后点击确定 
 
然后选择浏览相关内存区域 
 
然后选择以8字节十六进制显示 
 
然后对比源码，只要是看绿框的TUObjectArray类型 
 
然后接下来对比TUObjectArray类型，然后看FUObjectItem类型 
 
FUObjectItem** 这样的写法说明内存地址里存放的是一个内存地址，然后内存地址里放的还是内存地址，最终指向一个以FUObjectItem结构存放的内存数据，鼠标单击下图红框，然后按空格键 
 
然后就进入了1DA8F737B40这个内存地址了，然后上方说，内存地址里放的还是内存地址 
 
然后单击下图红框，然后再按空格键进入1DA903B0008内存地址 
 
然后下图就是以FUObjectItem结构存放的数据了 
 
然后对比源码，到这可以应该是可以更深入的理解数据结构这个概念了 
 
然后鼠标右击选择后退，后退到TUObjectArray里也就是FChunkedFixedUObjectArray里 
 
下图红框的代码 
 
代码说明，里面的元素概念指的是FUObjectItem，然后FUObjectItem存放的是UObject，然后UObject指的是角色、武器、道具、组件等游戏中的东西，然后块的概念是可以存放多少个FUObjectItem 

```text
/** 主表：指向多个"块"的总目录（二级指针数组）
 *  关系：
 *  - 每个"块"（Chunk）是一个数组，里面装着多个"元素"（FUObjectItem）
 *  - 主表（Objects）就像"仓库货架清单"，清单上的每个条目都指向一个货架（块）
 *  - 通过主表能快速找到所有货架，再从货架上找到具体的元素
 */
FUObjectItem** Objects;

/** 预分配的连续内存块：所有元素集中存放的"超级货架"
 *  关系：
 *  - 这是一块连续的内存，里面直接按顺序放着多个"元素"（FUObjectItem）
 *  - 和上面的"多块分散存储"不同，这里是"一块集中存储"，访问速度更快
 *  - 相当于把所有标签（元素）都整齐地放在一个超大盒子里，而不是多个小盒子
 */
FUObjectItem* PreAllocatedObjects;

/** 最大元素数量：系统能管理的最多"元素"总数
 *  关系：
 *  - "元素"（Element）就是单个FUObjectItem，每个对应一个游戏对象（UObject）
 *  - 这个值是上限，比如"最多能有10000个标签"，不管这些标签放在多少个块里
 */
int32 MaxElements;

/** 当前元素数量：现在实际存在的"元素"总数
 *  关系：
 *  - 等于所有块里的元素数量相加（比如3个块各有100、200、300个元素，总数就是600）
 *  - 每个元素对应一个真实的游戏对象，这个数越多，说明当前加载的对象越多
 */
int32 NumElements;

/** 最大块数量：主表（Objects）能容纳的最多"块"总数
 *  关系：
 *  - "块"（Chunk）是装元素的容器（数组），比如"最多能有10个盒子"
 *  - 超过这个数就需要扩容主表，否则无法新增块
 */
int32 MaxChunks;

/** 当前块数量：现在实际存在的"块"总数
 *  关系：
 *  - 每个块里都装着若干元素（比如当前有5个盒子，每个盒子里装着不同数量的标签）
 *  - 当元素数量增加，现有块装不下时，会新增块（这个数会增加）
 */
int32 NumChunks;

```
 
然后以4字节十进制的方式查看 
 
如下图，可以看出当前游戏的最大元素是2162688，当前元素数量是47681个，然后最大块是33，当前块的数量是1，如果切换地图它的数量会有变化 
 
然后它现在变成了52841个元素了，添加了5千多个以FUObjectItem结构存放的数据（FUObjectItem对象） 
 
然后记录一下偏移，TUObjectArray在FUObjectArray中0x10位置，FUObjectArray的位置是游戏基址+上一个内容找到的0x4A92740，也就是说最终的公式 游戏基址 + 0x4A92740 +0x10=TUObjectArray 
 
下一节将要Dump（下载存储）这些内存数据

## 12. 12.UE-游戏逆向-DumpUE对象

- URL: https://jisuanjiwang.blog.csdn.net/article/details/152418550
- Description: æç« æµè§éè¯»2.1kæ¬¡ï¼ç¹èµ20æ¬¡ï¼æ¶è15æ¬¡ãUE UnrealEngine4 èå¹»å¼æ æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_ueéå

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：11.UE-游戏逆向-内存中的FUObjectArray（深入理解内存数据） 
本次来保存游戏中的ue对象，主要需要的东西是下图红框UObjectBase里面的变量 
 
UObjectBase里面有虚函数 
 
主要用到的变量是下图红框的3个 
 
代码说明

```text
/** 用于跟踪和记录对象各种状态的标志（枚举类型）
 *  说明：
 *  - EObjectFlags是一个枚举，里面定义了很多"状态位"（比如"对象是否已加载"、"是否需要被垃圾回收"、"是否是临时对象"等）
 *  - 这些标志就像对象的"状态标签"，系统通过检查这些标签快速判断对象的当前状态
 *  - 特别处理：在32位系统上需要8字节对齐（内存对齐），避免内存浪费
 */
EObjectFlags					ObjectFlags;

/** 全局对象数组（GObjectArray）中的索引，非常私密的内部标识
 *  说明：
 *  - GObjectArray是UE管理所有对象的"总名单"，每个对象在这个名单里都有一个唯一位置
 *  - InternalIndex就是这个位置的编号（类似"学号"），系统通过这个编号能直接找到对象在数组中的位置，速度极快
 *  - "非常私有"表示这个值只在引擎内部使用，开发者一般不需要手动修改
 */
int32							InternalIndex;

/** 对象所属的类（类的元数据指针）
 *  说明：
 *  - UClass是UE中"类"的描述类型（比如"玩家类"、"武器类"的元信息都存在UClass里）
 *  - ClassPrivate指向当前对象的"模板类"，比如一个玩家对象的ClassPrivate就指向"玩家类"的UClass
 *  - 作用：通过它可以知道"这个对象是什么类型的"，以及这个类型有哪些功能（函数、属性等）
 */
UClass*							ClassPrivate;

/** 这个对象的名字
 *  说明：
 *  - FName是UE的高效名字类型（由GName系统管理，全局唯一，不重复存储）
 *  - NamePrivate存储对象的名称，比如"Player_01"、"Sword_03"，方便开发者识别对象
 *  - 和普通字符串不同，FName通过索引管理，比较和查找速度极快
 */
FName							NamePrivate;

/** 这个对象所在的"外部对象"（所有者或容器）
 *  说明：
 *  - OuterPrivate表示当前对象的"上级容器"或"所有者"，形成对象间的层级关系
 *  - 举例：一个武器组件（UObject）的OuterPrivate可能指向它所属的角色对象（另一个UObject）
 *  - 作用：管理对象的生命周期（当所有者被销毁时，它包含的对象也可能被销毁），以及组织对象的层级结构
 */
UObject*						OuterPrivate;

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：11.UE-游戏逆向-内存中的FUObjectArray（深入理解内存数据） 
本次来保存游戏中的ue对象，主要需要的东西是下图红框UObjectBase里面的变量 
 
UObjectBase里面有虚函数 
 
主要用到的变量是下图红框的3个 
 
代码说明 

```text
/** 用于跟踪和记录对象各种状态的标志（枚举类型）
 *  说明：
 *  - EObjectFlags是一个枚举，里面定义了很多"状态位"（比如"对象是否已加载"、"是否需要被垃圾回收"、"是否是临时对象"等）
 *  - 这些标志就像对象的"状态标签"，系统通过检查这些标签快速判断对象的当前状态
 *  - 特别处理：在32位系统上需要8字节对齐（内存对齐），避免内存浪费
 */
EObjectFlags					ObjectFlags;

/** 全局对象数组（GObjectArray）中的索引，非常私密的内部标识
 *  说明：
 *  - GObjectArray是UE管理所有对象的"总名单"，每个对象在这个名单里都有一个唯一位置
 *  - InternalIndex就是这个位置的编号（类似"学号"），系统通过这个编号能直接找到对象在数组中的位置，速度极快
 *  - "非常私有"表示这个值只在引擎内部使用，开发者一般不需要手动修改
 */
int32							InternalIndex;

/** 对象所属的类（类的元数据指针）
 *  说明：
 *  - UClass是UE中"类"的描述类型（比如"玩家类"、"武器类"的元信息都存在UClass里）
 *  - ClassPrivate指向当前对象的"模板类"，比如一个玩家对象的ClassPrivate就指向"玩家类"的UClass
 *  - 作用：通过它可以知道"这个对象是什么类型的"，以及这个类型有哪些功能（函数、属性等）
 */
UClass*							ClassPrivate;

/** 这个对象的名字
 *  说明：
 *  - FName是UE的高效名字类型（由GName系统管理，全局唯一，不重复存储）
 *  - NamePrivate存储对象的名称，比如"Player_01"、"Sword_03"，方便开发者识别对象
 *  - 和普通字符串不同，FName通过索引管理，比较和查找速度极快
 */
FName							NamePrivate;

/** 这个对象所在的"外部对象"（所有者或容器）
 *  说明：
 *  - OuterPrivate表示当前对象的"上级容器"或"所有者"，形成对象间的层级关系
 *  - 举例：一个武器组件（UObject）的OuterPrivate可能指向它所属的角色对象（另一个UObject）
 *  - 作用：管理对象的生命周期（当所有者被销毁时，它包含的对象也可能被销毁），以及组织对象的层级结构
 */
UObject*						OuterPrivate;

```
 
这里有个东西，FName它有里面有一个字符串的索引（id），这里可以使用CE找到UObjectBase类型的值，然后查看NamePrivate的值，然后使用之前实现的GName算法来看看它的FName是什么，首先使用0x4A92740偏移来到FUObjectArray 
 
然后单击下图红框，然后按空格进入TUObjectArray结构，注意下图红框是FUObjectArray+0x10位置 
 
然后进入TUObjectArray里的FUObjectItem**，也就是单击下图红框，然后按空格 
 
按完空格后就进入了FUObjectItem**结构的数据 
 
下图红框都是一个UObjectBase结构的内存地址 
 
然后使用鼠标进行选中，按一下CTRL+C进行复制 
 
然后如下图选择工具里的分析数据/遍历 
 
然后把复制的东西粘贴到下图红框位置 
 
然后选择定义新的结构 
 
下图红框随便写，然后点击确定 
 
然后就可以看到下图绿框是一个id，这个id就可以进行搜索 
 
这个数字可能是十六进制显示的，如下图选择4字节就会以十进制显示，id是十进制的 
 
然后使用我们的GName解密，如下图可以看到1097好像是一个路径 
 
到这应该会很蒙，又是FUObjectItem又是UObjectBase这都什么玩意，刚开始蒙就对了，现在应该有一点了解UObjectBase这个结构，但感觉差点事，现在应该是这种感觉，下面来整理一下 
 
 这一切都是从第10节，查找UObject开始，最开始说UObject是UE中所有 “可被引擎管理的对象” 的基类资源对象，就是武器、人物、材质、组件这些对象（对象就是对某个结构的数据在内存中的称呼），然后找UObject是通过vs2022搜索GUObjectArray这个关键字，就找到了FUObjectArray结构，这个FUObjectArray结构是用来记录UObject的，然后就开始分析FUObjectArray，它偏移0x10位置有个TUObjectArray类型，较早之前是使用FUObjectArray来实现UObject的记录和管理，但是FUObjectArray它不是很好，所以就有了TUObjectArray类型来代替FUObjectArray，TUObjectArray里面就有FUObjectItem，FUObjectItem对应一个UObject（UObjectBase），FUObjectItem里面记录的是UObject的地址，UObject是UObjectBase的升级版，它里面有，如下的白话解释 
 UObjectBase 里的信息不多，但每一条都是 “必须项”，少了它，小区（引擎）就不认这个住户（UObject）： 
  「身份标签」（ObjectFlags） 类似身份证上的 “状态标记”，比如 “是否有效”“是否临时住户”“是否需要注销”。引擎通过这些标签快速判断这个对象的基础状态（比如 “这户是不是已经搬走了？”）。  「全局编号」（InternalIndex） 小区给每户分配的唯一编号（比如 “XQ2023001”），和 TUObjectArray 登记本里的编号对应。引擎查这个号，能立刻在登记本里找到这户的详细记录（FUObjectItem）。  「所属类型」（ClassPrivate） 记录这户是 “什么类型的住户”，比如 “居民户”“商户”“物业办公室”。对应到游戏里，就是记录这个 UObject 属于哪个类（比如 “角色类”“道具类”），让引擎知道它能做什么（有哪些功能）。  「住户姓名」（NamePrivate） 这户的名字（比如 “张三家”“便民超市”），用 FName 类型存储（全局唯一，不会重名）。方便开发者在编辑器里识别对象（比如在蓝图里看到 “Player_01” 就知道是哪个角色）。  「所属上级」（OuterPrivate） 记录这户 “归谁管”，比如 “3 单元 201 室归 3 单元楼长管”。游戏里就是对象的 “上级容器”（比如 “武器组件” 归 “角色” 管），确保对象的层级关系清晰，方便批量管理（比如角色删除了，它的武器也跟着删）。   
 
这个东西就是很乱，想不乱只能多写多看，有一个dump代码是用来把游戏中的对象、函数、名字、内存中的地址保存到硬盘上的，上方的不理解也没事都是些理论，实际上用起来并没有那么多事 
需要改的位置，代码的原理就是先获取GName，然后通过上方的公式 
 
 FUObjectArray+0x10位置读取TUObjectArray 
 然后再从TUObjectArray+0x14位置获取当前元素的数量 
 然后从TUObjectArray+0x18位置获取当前块的数量 
 然后从TUObjectArray=0x0位置获取FUObjectItem 
 FUObjectItem里有0x14大小，在内存里有内存对齐，它会变成0x18 
 然后从FUObjectItem里得到UObjectBase 
 然后从UObjectBase+0x10位置获取Class 
 然后从UObjectBase+0x18位置获取FName也就是名字 
 然后从0x20位置获取UObject也就是对象 
 
 
文件保存在下图红框的目录里 
 
效果图：保存所有的对象的地址

## 13. 13.UE-游戏逆向-DumpUE Enum（枚举-UE对象Dump代码）

- URL: https://jisuanjiwang.blog.csdn.net/article/details/152509180
- Description: æç« æµè§éè¯»674æ¬¡ï¼ç¹èµ13æ¬¡ï¼æ¶è10æ¬¡ãèå¹»å¼æ UnrealEngine4 æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_uedump

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：12.UE-游戏逆向-DumpUE对象 
首先了解一个东西UObject继承UObjectBaseUtility类型 
 
然后UObjectBaseUtility继承UObjectBase类型，所以之前说UObjectBase就是UObject 
 
然后UObjectBase里面有下图红框的三个变量，上一个内容里也通过内存的方式去找了 
 
UObject现在知道是一个UObjectBase了，然后UClass还不知道，UClass继承于UStruct 
 
然后UStruct继承于UField 
 
然后UField继承于UObject，所以说Class也是一个UObjectBase，效果就是可以通过ClassPrivate变量得到类型的名字 
 
如下图的内容，它由空格隔开了三列，然后第一列对象地址它是通过取UObjectBase类型地址得到的，然后类型名是通过UObjectBase类型里面的ClassPrivate得到的（UClass继承于UObjectBase，本质上还是通过UObjectBase得到的），父类名是通过UObjectBase类型里面的OuterPrivate来得到的，注意这里的父类名并不是实际上用C++语法那样继承的父类，这里的父类只是一个逻辑上的，仅仅是UObjectBase类型里的一个名字，所以并不能再UE源码中找到对应的继承关系 
 
枚举，也是一个UObjectBase类型，在UE中定义枚举要用下图红框的代码UENUM(BlueprintType)然后下一行是enum class XXXX{}，这是C++声明枚举的方式，但是前面加了UENUM(BlueprintType)后UE会把后面的enum搞成UEnum类型 
 
然后UEnum继承UField，最终也会继承UObjectBase类型，所以它也有GName，它的GName是枚举的名字信息 
 
在UEnum+0x40位置是枚举的值和名字，如下图0x40位置是一个内存地址，内存地址里的数据是一个数组类型 
 
然后2631559这个id对应的字符串 
 
所以就有了，下方的结构 

```text
struct {
    uint16_t Name = 0x0;// 枚举里的名字
    uint16_t Value = 0x8;// 枚举的值
    uint16_t Size = 0x10;//Name结构体大小，16字节
    uint16_t Names = 0x40;//存放Names的指针位置，这个是指UEnum+0x40位置
} UEnum;

```
 
效果图： 
 
 
完整代码： 
 
 看置顶文章里的百度网盘链接

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：12.UE-游戏逆向-DumpUE对象 
首先了解一个东西UObject继承UObjectBaseUtility类型 
 
然后UObjectBaseUtility继承UObjectBase类型，所以之前说UObjectBase就是UObject 
 
然后UObjectBase里面有下图红框的三个变量，上一个内容里也通过内存的方式去找了 
 
UObject现在知道是一个UObjectBase了，然后UClass还不知道，UClass继承于UStruct 
 
然后UStruct继承于UField 
 
然后UField继承于UObject，所以说Class也是一个UObjectBase，效果就是可以通过ClassPrivate变量得到类型的名字 
 
如下图的内容，它由空格隔开了三列，然后第一列对象地址它是通过取UObjectBase类型地址得到的，然后类型名是通过UObjectBase类型里面的ClassPrivate得到的（UClass继承于UObjectBase，本质上还是通过UObjectBase得到的），父类名是通过UObjectBase类型里面的OuterPrivate来得到的，注意这里的父类名并不是实际上用C++语法那样继承的父类，这里的父类只是一个逻辑上的，仅仅是UObjectBase类型里的一个名字，所以并不能再UE源码中找到对应的继承关系 
 
枚举，也是一个UObjectBase类型，在UE中定义枚举要用下图红框的代码UENUM(BlueprintType)然后下一行是enum class XXXX{}，这是C++声明枚举的方式，但是前面加了UENUM(BlueprintType)后UE会把后面的enum搞成UEnum类型 
 
然后UEnum继承UField，最终也会继承UObjectBase类型，所以它也有GName，它的GName是枚举的名字信息 
 
在UEnum+0x40位置是枚举的值和名字，如下图0x40位置是一个内存地址，内存地址里的数据是一个数组类型 
 
然后2631559这个id对应的字符串 
 
所以就有了，下方的结构 

```text
struct {
    uint16_t Name = 0x0;// 枚举里的名字
    uint16_t Value = 0x8;// 枚举的值
    uint16_t Size = 0x10;//Name结构体大小，16字节
    uint16_t Names = 0x40;//存放Names的指针位置，这个是指UEnum+0x40位置
} UEnum;

```
 
效果图： 
 
 
完整代码： 
 
 看置顶文章里的百度网盘链接

## 14. 14.UE-游戏逆向-DumpUE Function

- URL: https://jisuanjiwang.blog.csdn.net/article/details/152814571
- Description: æç« æµè§éè¯»907æ¬¡ï¼ç¹èµ5æ¬¡ï¼æ¶è3æ¬¡ãèå¹»å¼æ UnrealEngine4 æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_ue5 dump

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：13.UE-游戏逆向-DumpUE Enum（枚举-UE对象Dump代码） 
Function也就是下图红框的这种东西，随便复制一个Function的地址 
 
这里用的 0x0000022E3A6EB3E0 地址，也就是上图红框里的地址，然后把它拿到CE里，点击浏览相关内存区域 
 
然后选择下图红框 
 
然后点击 定义新的结构 
 
然后在下图红框随便输入一个名字 
 
然后如下图红框找7F开头的地址，7F开头的是全局的 
 
开头是什么取决于，如下图红框使用文件名得到的地址的开头，也就是基址的开头 
 
然后在结构的D8位置就是函数 
 
它怎么就是函数地址了，双击下图红框位置 
 
会弹出对话框，然后可以复制这个地址 7FF727915C50 
 
然后点击下图红框任意位置，然后按CTRL+G就会弹出下图转到地址的弹框，然后在蓝框里输入上方复制的地址，然后点击确定 
 
然后就根据地址跳转到了一段代码，如下图红框，一眼看过去就能很清晰的认识到它是一个函数头部（看的多了就知道了） 
 
然后在Dump代码中下图红框位置实现的Dump函数 
 
如下图运行后 
 
文件内容

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：13.UE-游戏逆向-DumpUE Enum（枚举-UE对象Dump代码） 
Function也就是下图红框的这种东西，随便复制一个Function的地址 
 
这里用的 0x0000022E3A6EB3E0 地址，也就是上图红框里的地址，然后把它拿到CE里，点击浏览相关内存区域 
 
然后选择下图红框 
 
然后点击 定义新的结构 
 
然后在下图红框随便输入一个名字 
 
然后如下图红框找7F开头的地址，7F开头的是全局的 
 
开头是什么取决于，如下图红框使用文件名得到的地址的开头，也就是基址的开头 
 
然后在结构的D8位置就是函数 
 
它怎么就是函数地址了，双击下图红框位置 
 
会弹出对话框，然后可以复制这个地址 7FF727915C50 
 
然后点击下图红框任意位置，然后按CTRL+G就会弹出下图转到地址的弹框，然后在蓝框里输入上方复制的地址，然后点击确定 
 
然后就根据地址跳转到了一段代码，如下图红框，一眼看过去就能很清晰的认识到它是一个函数头部（看的多了就知道了） 
 
然后在Dump代码中下图红框位置实现的Dump函数 
 
如下图运行后 
 
文件内容

## 15. 15.UE-游戏逆向-DumpUE struct

- URL: https://jisuanjiwang.blog.csdn.net/article/details/152947841
- Description: æç« æµè§éè¯»1.7kæ¬¡ï¼ç¹èµ21æ¬¡ï¼æ¶è13æ¬¡ãèå¹» UE UnrealEngine4 æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_ue5éå

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：14.UE-游戏逆向-DumpUE Function 
struct需要知道下方的三个东西 
 
 UStruct、FField、FProperty 
 UStruct是一个用来描述结构体的东西，它就相当于下方的代码，就是一个类，然后这里面只有数据，数据是使用FField结构来描述的，FProperty是基于FField实现的，FField里面只有基本信息，比如成员变量的名称，然后成员变量的值是通过FProperty结构存储的，这里的FProperty是一个抽象，它有好多实现 
 
```text
class c{}

```
 
 如下图红框FProperty的多个实现，下图红框只是一部分 
 
 
接下来就来找UStruct、FField、FProperty这三个东西，然后通过CoreUObject.Vector来找，它是坐标的结构（x、y、z），它们的类型是float是4字节，然后3个4字节是12字节 
 
还是使用ce的结构分析来找 
 
下图红框指向的是FProperty，这里CE它分析错了，下图红框应该是个指针是个地址 
 
然后在0x50位置右击选择指针，如下图可以看到0x50位置的值是1AE23656F00这与其它的地址开头是一样的，所以就可以认定是CE分析的有问题，把地址分析成了普通数据 
 
然后选中0x51到0x54，右击选择删除 
 
然后就可以了，下图的0x58是结构的大小3个4字节正好是12，然后0x50是指向的第一个成员变量，也就是一个FProperty（看到FProperty要知道包含了FField，因为FProperty基于FField实现的） 
 
然后struct中还有一个SuperStruct，它使用来指向父struct的，这个CoreUObject.Vector没有，需要看CoreUObject.Struct这个结构它的SuperStruct指向CoreUObject.Field的地址，然后如下图就找CoreUObject.Struct的地址 
 
下图是CoreUObject.Struct结构的内存，SuperStruct在0x40位置，如下图红框，为什么在0x40 
 
如下图红框0x40位置的地址是可以和CoreUObject.Field的地址对上 
 
然后struct就没别的需要知道的了，然后是FProperty，再次回到CoreUObject.Vector的内存，如下图点开0x50 
 
然后成员变量的名字，如下图0x28位置是成员变量的名字，它是一个GName的id 
 
如下图67950对应的字符串是x 
 
下一个FProperty在0x20位置，如下图CE也把它分析错了 
 
然后下图红框就是下一个成员变量，也就是y 
 
可以通过0x28位置的GName的id来确认 
 
如下图红框是Y 
 
然后数据大小和偏移，0x3C位置的值是数据类型的大小，0x4C是偏移 
 
然后是FProperty中的类（Class），是0x8位置，它与游戏基址开头一样都是7F，然后0x0位置是虚函数 
 
然后是FProperty的大小，FProperty指的就是 CoreUObject.Property，想知道FProperty的大小需要进入CoreUObject.Property的内存，如下图红框它的内存地址 
 
它的大小在0x58位置是0x78，下方的内存分析的有问题，FProperty的大小是0x78 
 
以上的结构位置记住就行，UE4和UE5通杀，就算位置变了也不会有太大的变化

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：14.UE-游戏逆向-DumpUE Function 
struct需要知道下方的三个东西 
 
 UStruct、FField、FProperty 
 UStruct是一个用来描述结构体的东西，它就相当于下方的代码，就是一个类，然后这里面只有数据，数据是使用FField结构来描述的，FProperty是基于FField实现的，FField里面只有基本信息，比如成员变量的名称，然后成员变量的值是通过FProperty结构存储的，这里的FProperty是一个抽象，它有好多实现 
 
```text
class c{}

```
 
 如下图红框FProperty的多个实现，下图红框只是一部分 
 
 
接下来就来找UStruct、FField、FProperty这三个东西，然后通过CoreUObject.Vector来找，它是坐标的结构（x、y、z），它们的类型是float是4字节，然后3个4字节是12字节 
 
还是使用ce的结构分析来找 
 
下图红框指向的是FProperty，这里CE它分析错了，下图红框应该是个指针是个地址 
 
然后在0x50位置右击选择指针，如下图可以看到0x50位置的值是1AE23656F00这与其它的地址开头是一样的，所以就可以认定是CE分析的有问题，把地址分析成了普通数据 
 
然后选中0x51到0x54，右击选择删除 
 
然后就可以了，下图的0x58是结构的大小3个4字节正好是12，然后0x50是指向的第一个成员变量，也就是一个FProperty（看到FProperty要知道包含了FField，因为FProperty基于FField实现的） 
 
然后struct中还有一个SuperStruct，它使用来指向父struct的，这个CoreUObject.Vector没有，需要看CoreUObject.Struct这个结构它的SuperStruct指向CoreUObject.Field的地址，然后如下图就找CoreUObject.Struct的地址 
 
下图是CoreUObject.Struct结构的内存，SuperStruct在0x40位置，如下图红框，为什么在0x40 
 
如下图红框0x40位置的地址是可以和CoreUObject.Field的地址对上 
 
然后struct就没别的需要知道的了，然后是FProperty，再次回到CoreUObject.Vector的内存，如下图点开0x50 
 
然后成员变量的名字，如下图0x28位置是成员变量的名字，它是一个GName的id 
 
如下图67950对应的字符串是x 
 
下一个FProperty在0x20位置，如下图CE也把它分析错了 
 
然后下图红框就是下一个成员变量，也就是y 
 
可以通过0x28位置的GName的id来确认 
 
如下图红框是Y 
 
然后数据大小和偏移，0x3C位置的值是数据类型的大小，0x4C是偏移 
 
然后是FProperty中的类（Class），是0x8位置，它与游戏基址开头一样都是7F，然后0x0位置是虚函数 
 
然后是FProperty的大小，FProperty指的就是 CoreUObject.Property，想知道FProperty的大小需要进入CoreUObject.Property的内存，如下图红框它的内存地址 
 
它的大小在0x58位置是0x78，下方的内存分析的有问题，FProperty的大小是0x78 
 
以上的结构位置记住就行，UE4和UE5通杀，就算位置变了也不会有太大的变化

## 16. 16.UE-游戏逆向-查找UWorld

- URL: https://jisuanjiwang.blog.csdn.net/article/details/153079615
- Description: æç« æµè§éè¯»1.6kæ¬¡ï¼ç¹èµ5æ¬¡ï¼æ¶è8æ¬¡ãèå¹»å¼æ UE4 UnrealEngine4 æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_gname uworld

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：15.UE-游戏逆向-DumpUE struct 
UWorld是一个类型，它是一个全局的，在UE中这个UWorld类型的变量名叫做GWorld，所以说GWorld就是UWorld 
为什么要找GWorld，因为需要找游戏中的数据，比如周围的人物道具、关卡信息，物理模拟、时间管理、环境设置 
 
 周围的人物道具：在UE中叫做Actor，它可以是角色、敌人、道具等 
 关卡信息：在UE中叫做Level，它是用来管理关卡的加载和卸载和关卡之间的切换，每个关卡都会有一个UWorld结构的数据 
 物理模拟：重力、碰撞检测等 
 时间管理：游戏中的时间流逝、暂停、恢复、改变时间速度等 
 环境设置：天空、光照等 
 
通过UWorld是UE4引擎中的类，不是开发者自己写的，UWorld可以很方便的管理上方（周围的人物道具、关卡信息，物理模拟、时间管理、环境设置）的内容，可以获取UE中的GWorld，通过获取到GWorld来访问当前UWorld实例 
下图是UWorld类的继承关系图 
 
然后怎么找GWorld，首先打开UE4的源码，如下图直接搜索GWorld 
 
找Source里的Runtime里的Engine里的Privvate 
 
然后找UnrealEngine.cpp里的下图蓝框的代码，找到后双击下图蓝框里的内容 
 
双击完就会跳转到下图红框的代码中 
 
然后可以使用下图红框的字符串定位GWorld的地址 
 
然后使用ida反编译游戏的exe文件，然后使用names进行搜索，如下图什么都搜不出来，这个愿意是它会把空格过滤掉 
 
如下图红框把空格删了，然后再删几个字符串就可以找到了，然后双击下图蓝框 
 
然后如下图蓝框，就跳转到了字符串的位置，然后双击下图红框 
 
然后如下图 
 
然后按F5，就能看到下图的函数 
 
然后对比UE4的源码，很显然，下图红框里的return的内容是GWorld，也就是144BDAAC0 
 
然后游戏的基址是0x140000000，基址是会变的，所以要0x144BDAAC0-0x140000000，结果就是4BDAAC0，这样就找到了UWorld了，现在GName、GObject、UWorld都找到了，后面就可以通过它们得到想要的数据了

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：15.UE-游戏逆向-DumpUE struct 
UWorld是一个类型，它是一个全局的，在UE中这个UWorld类型的变量名叫做GWorld，所以说GWorld就是UWorld 
为什么要找GWorld，因为需要找游戏中的数据，比如周围的人物道具、关卡信息，物理模拟、时间管理、环境设置 
 
 周围的人物道具：在UE中叫做Actor，它可以是角色、敌人、道具等 
 关卡信息：在UE中叫做Level，它是用来管理关卡的加载和卸载和关卡之间的切换，每个关卡都会有一个UWorld结构的数据 
 物理模拟：重力、碰撞检测等 
 时间管理：游戏中的时间流逝、暂停、恢复、改变时间速度等 
 环境设置：天空、光照等 
 
通过UWorld是UE4引擎中的类，不是开发者自己写的，UWorld可以很方便的管理上方（周围的人物道具、关卡信息，物理模拟、时间管理、环境设置）的内容，可以获取UE中的GWorld，通过获取到GWorld来访问当前UWorld实例 
下图是UWorld类的继承关系图 
 
然后怎么找GWorld，首先打开UE4的源码，如下图直接搜索GWorld 
 
找Source里的Runtime里的Engine里的Privvate 
 
然后找UnrealEngine.cpp里的下图蓝框的代码，找到后双击下图蓝框里的内容 
 
双击完就会跳转到下图红框的代码中 
 
然后可以使用下图红框的字符串定位GWorld的地址 
 
然后使用ida反编译游戏的exe文件，然后使用names进行搜索，如下图什么都搜不出来，这个愿意是它会把空格过滤掉 
 
如下图红框把空格删了，然后再删几个字符串就可以找到了，然后双击下图蓝框 
 
然后如下图蓝框，就跳转到了字符串的位置，然后双击下图红框 
 
然后如下图 
 
然后按F5，就能看到下图的函数 
 
然后对比UE4的源码，很显然，下图红框里的return的内容是GWorld，也就是144BDAAC0 
 
然后游戏的基址是0x140000000，基址是会变的，所以要0x144BDAAC0-0x140000000，结果就是4BDAAC0，这样就找到了UWorld了，现在GName、GObject、UWorld都找到了，后面就可以通过它们得到想要的数据了

## 17. 17.UE-游戏逆向-查找Aactor（游戏中物品的名字和坐标）

- URL: https://jisuanjiwang.blog.csdn.net/article/details/153210404
- Description: æç« æµè§éè¯»1.4kæ¬¡ï¼ç¹èµ45æ¬¡ï¼æ¶è39æ¬¡ãèå¹»å¼æ UE4 UNrealEngine4 æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_ueéårootcomponentæä»ä¹

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：16.UE-游戏逆向-查找UWorld 
本次来理Aactor的结构，从而得到游戏中所有东西（怪物、树、角色等）的名字和坐标，也就是找UWorld-》ULevel-》AActor 
首先打开CE，使用上一个内容找到的UWorld的偏移（4BDAAC0），找到它的地址（公式：游戏的exe文件名+0x4BDAAC0），如下图红框UWorld的地址 
 
然后打开之前Dump的class，如下图找到ULevel的在UWorld中的偏移0x30 
 
然后鼠标右键选择浏览相关内存区域 
 
然后选择分析数据/遍历 
 
然后确认下图红框的内容是不是UWorld的地址 
 
然后点击定义新结构 
 
然后随便输入一个名字，然后点击确定 
 
然后就显示了UWorld的内存结构 
 
首先点击0x0位置，因为使用的是UWorld的地址找到的，需要看UWorld的内容，也就是内存地址里面的值，然后再点击0x30位置，如下图红框的，然后就可以看到下图蓝框的内容 
 
上图蓝框的内容就是下图红框里面的内容了 
 
然后如下图红框再找ULevel，查看它里面的结构，然后上一个内容里写了ULevel里有一个Actors的变量，但是下图中没有， 这怎么办 
 
Actors是一个TArray的类型，可以通过TArray的特征在ULevel中找，TArray是一个数据一个是当前存放的多少数据一个是最大可以存放多少数据，所以就可以根据这个特征去看内存，如下图红框它有多个位置符合特征，哪一个才是？ 
 
当前的游戏处在主菜单界面，没有进入游戏中，接下来进入游戏，进入游戏后当前存放的多少数据的值会变大，可存放的最大数据也会变大，所以就找进入游戏后会变化的那一个，会变的很大很，会有大上万上千个，起码最少一千个，如下图进入游戏地图后，变大了 
 
然后点开它，如下图红框就是游戏中的树、怪物、建筑物等，在游戏中可以看到的和看不到的都可以在这里找到，注意下图红框全是内存地址，AActor结构的内存地址，如果不是内存地址说明CE分析错了，只需要右击选择指针类型即可 
 
然后分析它的名字，它的名字也是一个GName，也就是一个id，找符合id的数据，下图红框的就符合GName的id，注意现在所在的结构是一个 AActor 
 
如下图C791的字符串，正常来说名字不可能这么长，所以它并不是名字 
 
然后是2E65d5，SM_wb_world_01这应该是地图的名字 
 
然后在看其它的，如下图这是一个树的id，tree_blender4正常来说它是第4个树 
 
然后现在找到名字了，接下来查看它的坐标，看下图红框里的数据，也就是tree_blender4的数据，通过它来找坐标，坐标是在RootComponent里面（根组件） 
 
然后就来到0x130的位置，这里CE分析的有问题， 
 
然后在0x1D0位置就可以看到坐标了，游戏中树木很多，修改之后可能看不出什么效果，后面使用代码把它们全部遍历出来，然后再搞 
 
到这可以理解万物都是对象，都是Actor类型的对象

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：16.UE-游戏逆向-查找UWorld 
本次来理Aactor的结构，从而得到游戏中所有东西（怪物、树、角色等）的名字和坐标，也就是找UWorld-》ULevel-》AActor 
首先打开CE，使用上一个内容找到的UWorld的偏移（4BDAAC0），找到它的地址（公式：游戏的exe文件名+0x4BDAAC0），如下图红框UWorld的地址 
 
然后打开之前Dump的class，如下图找到ULevel的在UWorld中的偏移0x30 
 
然后鼠标右键选择浏览相关内存区域 
 
然后选择分析数据/遍历 
 
然后确认下图红框的内容是不是UWorld的地址 
 
然后点击定义新结构 
 
然后随便输入一个名字，然后点击确定 
 
然后就显示了UWorld的内存结构 
 
首先点击0x0位置，因为使用的是UWorld的地址找到的，需要看UWorld的内容，也就是内存地址里面的值，然后再点击0x30位置，如下图红框的，然后就可以看到下图蓝框的内容 
 
上图蓝框的内容就是下图红框里面的内容了 
 
然后如下图红框再找ULevel，查看它里面的结构，然后上一个内容里写了ULevel里有一个Actors的变量，但是下图中没有， 这怎么办 
 
Actors是一个TArray的类型，可以通过TArray的特征在ULevel中找，TArray是一个数据一个是当前存放的多少数据一个是最大可以存放多少数据，所以就可以根据这个特征去看内存，如下图红框它有多个位置符合特征，哪一个才是？ 
 
当前的游戏处在主菜单界面，没有进入游戏中，接下来进入游戏，进入游戏后当前存放的多少数据的值会变大，可存放的最大数据也会变大，所以就找进入游戏后会变化的那一个，会变的很大很，会有大上万上千个，起码最少一千个，如下图进入游戏地图后，变大了 
 
然后点开它，如下图红框就是游戏中的树、怪物、建筑物等，在游戏中可以看到的和看不到的都可以在这里找到，注意下图红框全是内存地址，AActor结构的内存地址，如果不是内存地址说明CE分析错了，只需要右击选择指针类型即可 
 
然后分析它的名字，它的名字也是一个GName，也就是一个id，找符合id的数据，下图红框的就符合GName的id，注意现在所在的结构是一个 AActor 
 
如下图C791的字符串，正常来说名字不可能这么长，所以它并不是名字 
 
然后是2E65d5，SM_wb_world_01这应该是地图的名字 
 
然后在看其它的，如下图这是一个树的id，tree_blender4正常来说它是第4个树 
 
然后现在找到名字了，接下来查看它的坐标，看下图红框里的数据，也就是tree_blender4的数据，通过它来找坐标，坐标是在RootComponent里面（根组件） 
 
然后就来到0x130的位置，这里CE分析的有问题， 
 
然后在0x1D0位置就可以看到坐标了，游戏中树木很多，修改之后可能看不出什么效果，后面使用代码把它们全部遍历出来，然后再搞 
 
到这可以理解万物都是对象，都是Actor类型的对象

## 18. 18.UE-游戏逆向-使用代码打印对象（Aactor）坐标

- URL: https://jisuanjiwang.blog.csdn.net/article/details/153271911
- Description: æç« æµè§éè¯»1kæ¬¡ï¼ç¹èµ9æ¬¡ï¼æ¶è5æ¬¡ãèå¹»å¼æ æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_ue5 éååæè·åç©å®¶èªå·±çåæ 

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：17.UE-游戏逆向-查找Aactor（游戏中物品的名字和坐标） 
在之前的IMGui的代码里添加下图红框的代码 
 
效果图：可以正常打印坐标 
 
代码：

```text
#include "main.h"

HWND hWnd = FindWindowA("UnrealWindow", NULL);

static ID3D11Device* g_pd3dDevice = nullptr;
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;
static IDXGISwapChain* g_pSwapChain = nullptr;
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;
DWORD64* VirtaulTable;

DWORD64 GWorld = (DWORD64)GetModuleHandleA("GWorld所在的模块名，也就是游戏的exe文件名") + 0x4BDAAC0;

typedef  HRESULT(STDMETHODCALLTYPE* Present)(
    IDXGISwapChain* This,
    /* [in] */ UINT SyncInterval,
    /* [in] */ UINT Flags);
Present MyPresent;

HRESULT VtPresent(
    IDXGISwapChain* This,
    /* [in] */ UINT SyncInterval,
    /* [in] */ UINT Flags) {

ImGui_ImplDX11_NewFrame();
    ImGui_ImplWin32_NewFrame();
    ImGui::NewFrame();

ImGui::Begin("Hello, world!");
    ImGui::End();
    
    // 得到 Aactors
    DWORD64 Aactor = *(DWORD64*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0x98);
    // 得到Aactor里内容的数量
    int Num = *(int*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0xa0);

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：17.UE-游戏逆向-查找Aactor（游戏中物品的名字和坐标） 
在之前的IMGui的代码里添加下图红框的代码 
 
效果图：可以正常打印坐标 
 
代码： 

```text
#include "main.h"

HWND hWnd = FindWindowA("UnrealWindow", NULL);

static ID3D11Device* g_pd3dDevice = nullptr;
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;
static IDXGISwapChain* g_pSwapChain = nullptr;
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;
DWORD64* VirtaulTable;

DWORD64 GWorld = (DWORD64)GetModuleHandleA("GWorld所在的模块名，也就是游戏的exe文件名") + 0x4BDAAC0;

typedef  HRESULT(STDMETHODCALLTYPE* Present)(
    IDXGISwapChain* This,
    /* [in] */ UINT SyncInterval,
    /* [in] */ UINT Flags);
Present MyPresent;

HRESULT VtPresent(
    IDXGISwapChain* This,
    /* [in] */ UINT SyncInterval,
    /* [in] */ UINT Flags) {

    ImGui_ImplDX11_NewFrame();
    ImGui_ImplWin32_NewFrame();
    ImGui::NewFrame();

    ImGui::Begin("Hello, world!");
    ImGui::End();
    
    // 得到 Aactors
    DWORD64 Aactor = *(DWORD64*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0x98);
    // 得到Aactor里内容的数量
    int Num = *(int*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0xa0);

    for (int i = 0; i < Num; i++)
    {
        //  *(DWORD64*)(Aactor + 8 * i) != 0意思是从Aactors里取一个数据，判断这个数据是不是存在，不等于0就存在
        if ((Aactor + 8 * i) != 0 && *(DWORD64*)(Aactor + 8 * i) != 0 && *(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) != 0) {
            // (*(DWORD64*)(Aactor + 8 * i) + 0x130)取出 RootComponent根组件
            // *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130)+0x1d0); 取出x坐标
           float x = *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130)+0x1d0);
           float y = *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130)+0x1d4);
           float z = *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130)+0x1d8);
           printf("x=%f,y=%f,z=%f\n", x, y, z);

        }
    }

    ImGui::Render();
    g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
    ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

    return MyPresent(This, SyncInterval, Flags);
}

extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
WNDPROC myWNDPROC;

LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;

   
    return ::CallWindowProc(myWNDPROC,hWnd, msg, wParam, lParam);
}
HRESULT Init(
    IDXGISwapChain* This,
    /* [in] */ UINT SyncInterval,
    /* [in] */ UINT Flags) {

    myWNDPROC = (WNDPROC)SetWindowLongPtrA(hWnd, GWLP_WNDPROC, (LONG_PTR)WndProc);
    
    This->GetDevice(_uuidof(g_pd3dDevice), (void**)&g_pd3dDevice);
    g_pd3dDevice->GetImmediateContext((ID3D11DeviceContext**) &g_pd3dDeviceContext);

    ID3D11Texture2D* pBackBuffer;
    This->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);
    pBackBuffer->Release();

    ImGui::CreateContext();
    ImGui::StyleColorsDark();
    ImGui_ImplWin32_Init(hWnd);
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);

    printf("HOOK");
    // hook Present函数，当执行Present函数时，让它去执行VtPresent函数
    VirtaulTable[8] = (DWORD64)VtPresent;
    return MyPresent(This, SyncInterval, Flags);
}

DWORD Go(
    LPVOID lpThreadParameter
) {
    
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));
    sd.BufferCount = 2;
    sd.BufferDesc.Width = 0;
    sd.BufferDesc.Height = 0;
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    sd.BufferDesc.RefreshRate.Numerator = 60;
    sd.BufferDesc.RefreshRate.Denominator = 1;
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
    sd.OutputWindow = hWnd;
    sd.SampleDesc.Count = 1;
    sd.SampleDesc.Quality = 0;
    sd.Windowed = TRUE;
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;

    UINT createDeviceFlags = 0;
    //createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;
    D3D_FEATURE_LEVEL featureLevel;
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0, };
    HRESULT res = D3D11CreateDeviceAndSwapChain(nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, createDeviceFlags, featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain, &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext);
    if (res == DXGI_ERROR_UNSUPPORTED) // Try high-performance WARP software driver if hardware is not available.
        res = D3D11CreateDeviceAndSwapChain(nullptr, D3D_DRIVER_TYPE_WARP, nullptr, createDeviceFlags, featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain, &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext);
    if (res != S_OK)
        return false;

    // 得到虚表
    VirtaulTable = *(DWORD64**)g_pSwapChain;
    // 得到虚函数Present的地址
    MyPresent = (Present)VirtaulTable[8];

    DWORD a;
    // 把VirtaulTable所在的内存页修改为可读可写可执行
    VirtualProtect(VirtaulTable,1, PAGE_EXECUTE_READWRITE, &a);
    VirtaulTable[8] = (DWORD64)Init;
    return 0;
}

```

## 19. 19.UE-游戏逆向-屏幕坐标转换

- URL: https://jisuanjiwang.blog.csdn.net/article/details/153415609
- Description: æç« æµè§éè¯»1.4kæ¬¡ï¼ç¹èµ8æ¬¡ï¼æ¶è8æ¬¡ãèå¹» UnrealEngine4 æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：18.UE-游戏逆向-使用代码打印对象（Aactor）坐标 
上一个内容里，通过获取游戏中的Aactor得到了坐标，然后这个坐标是游戏中的三维坐标，我们使用的看到的实际上是屏幕坐标，所以要把三维坐标转成屏幕坐标 
在UE中它有一个叫做ProjectWorldLocationToScreen的函数，通过函数名的中文翻译 世界坐标投影到屏幕坐标，也可以很清晰的看出它的作用，然后下图是通过Dump得到的，但是它Dump的有问题，所以需要进入UE4的源代码中进一步查看 
 
打开UE4源码后，然后进行搜索 
 
然后下图红框的就是了，直接鼠标左键双击下图红框 
 
如下图红框，它实际上有4个参数，第一个参数还是一个this（调用函数者的对象地址），然后第二个参数是世界坐标，第三个参数是屏幕坐标（传进一个存放屏幕坐标的地址，调用函数后会给里面添加好屏幕坐标） 
 
然后接下来找ProjectWorldToScreen的地址，首先使用ida反编译游戏的exe，然后复制ProjectWorldLocationToScreen的偏移 
 
然后来到ida按一下键盘上的G键，然后输入下图红框的内容，下图红框开头是14，开头具体是什么，参考下图蓝框中地址的开头，然后点击ok 
 
然后就跳转到了ProjectWorldLocationToScreen函数里，然后按F5 
 
然后找ProjectWorldToScreen，如下图红框只有它是4个参数并且它也是返回值，所以 sub_142BB56F0 是ProjectWorldToScreen的地址，偏移 2BB56F0，然后就找到了ProjectWorldToScreen 
 
然后开始写代码，首先要找一下，下图红框的两个结构体的内容 
 
如下图红框 
 
如下图红框，添加ProjectWorldToScreen类型的函数指针，用来调用游戏中的ProjectWorldToScreen函数，函数指针是一个数据类型，函数指针类型的值都会被当成一个函数地址 
 
完整代码

```text
#include "main.h"

// ScriptStruct  CoreUObject.Vector
// Struct Size::0x000C
struct FVector
{
    float                                         X;                                                            // 0x0000(0x0004)
    float                                         Y;                                                            // 0x0004(0x0004)
    float                                         Z;                                                            // 0x0008(0x0004)
};

// ScriptStruct  CoreUObject.Vector2D
// Struct Size::0x0008
struct FVector2D
{
    float                                         X;                                                            // 0x0000(0x0004)
    float                                         Y;                                                            // 0x0004(0x0004)
};

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：18.UE-游戏逆向-使用代码打印对象（Aactor）坐标 
上一个内容里，通过获取游戏中的Aactor得到了坐标，然后这个坐标是游戏中的三维坐标，我们使用的看到的实际上是屏幕坐标，所以要把三维坐标转成屏幕坐标 
在UE中它有一个叫做ProjectWorldLocationToScreen的函数，通过函数名的中文翻译 世界坐标投影到屏幕坐标，也可以很清晰的看出它的作用，然后下图是通过Dump得到的，但是它Dump的有问题，所以需要进入UE4的源代码中进一步查看 
 
打开UE4源码后，然后进行搜索 
 
然后下图红框的就是了，直接鼠标左键双击下图红框 
 
如下图红框，它实际上有4个参数，第一个参数还是一个this（调用函数者的对象地址），然后第二个参数是世界坐标，第三个参数是屏幕坐标（传进一个存放屏幕坐标的地址，调用函数后会给里面添加好屏幕坐标） 
 
然后接下来找ProjectWorldToScreen的地址，首先使用ida反编译游戏的exe，然后复制ProjectWorldLocationToScreen的偏移 
 
然后来到ida按一下键盘上的G键，然后输入下图红框的内容，下图红框开头是14，开头具体是什么，参考下图蓝框中地址的开头，然后点击ok 
 
然后就跳转到了ProjectWorldLocationToScreen函数里，然后按F5 
 
然后找ProjectWorldToScreen，如下图红框只有它是4个参数并且它也是返回值，所以 sub_142BB56F0 是ProjectWorldToScreen的地址，偏移 2BB56F0，然后就找到了ProjectWorldToScreen 
 
然后开始写代码，首先要找一下，下图红框的两个结构体的内容 
 
如下图红框 
 
如下图红框，添加ProjectWorldToScreen类型的函数指针，用来调用游戏中的ProjectWorldToScreen函数，函数指针是一个数据类型，函数指针类型的值都会被当成一个函数地址 
 
完整代码 

```text
#include "main.h"

// ScriptStruct  CoreUObject.Vector
// Struct Size::0x000C
struct FVector
{
    float                                         X;                                                            // 0x0000(0x0004)
    float                                         Y;                                                            // 0x0004(0x0004)
    float                                         Z;                                                            // 0x0008(0x0004)
};

// ScriptStruct  CoreUObject.Vector2D
// Struct Size::0x0008
struct FVector2D
{
    float                                         X;                                                            // 0x0000(0x0004)
    float                                         Y;                                                            // 0x0004(0x0004)
};

typedef bool (WINAPI* FN_ProjectWorldToScreen)(void * Player, FVector WorldLocation, FVector2D ScreenLocation, bool bPlayerViewportRelative);

HWND hWnd = FindWindowA("UnrealWindow", NULL);

static ID3D11Device* g_pd3dDevice = nullptr;
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;
static IDXGISwapChain* g_pSwapChain = nullptr;
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;
DWORD64* VirtaulTable;

DWORD64 GWorld = (DWORD64)GetModuleHandleA("xxx-Win64-Shipping.exe") + 0x4BDAAC0;

typedef  HRESULT(STDMETHODCALLTYPE* Present)(
    IDXGISwapChain* This,
    /* [in] */ UINT SyncInterval,
    /* [in] */ UINT Flags);
Present MyPresent;

HRESULT VtPresent(
    IDXGISwapChain* This,
    /* [in] */ UINT SyncInterval,
    /* [in] */ UINT Flags) {

    ImGui_ImplDX11_NewFrame();
    ImGui_ImplWin32_NewFrame();
    ImGui::NewFrame();

    ImGui::Begin("Hello, world!");
    ImGui::End();
    
    // 得到 Aactors
    DWORD64 Aactor = *(DWORD64*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0x98);
    // 得到Aactor里内容的数量
    int Num = *(int*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0xa0);

    FN_ProjectWorldToScreen My_ProjectWorldLocationToScreen = (FN_ProjectWorldToScreen)(0x2BB56F0 + (DWORD64)GetModuleHandleA("xxxxxx-Win64-Shipping.exe"));

    for (int i = 0; i < Num; i++)
    {
        //  *(DWORD64*)(Aactor + 8 * i) != 0意思是从Aactors里取一个数据，判断这个数据是不是存在，不等于0就存在
        if ((Aactor + 8 * i) != 0 && *(DWORD64*)(Aactor + 8 * i) != 0 && *(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) != 0) {
            // (*(DWORD64*)(Aactor + 8 * i) + 0x130)取出 RootComponent根组件
            // *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130)+0x1d0); 取出x坐标
           float x = *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130)+0x1d0);
           float y = *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130)+0x1d4);
           float z = *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130)+0x1d8);
           printf("x=%f,y=%f,z=%f\n", x, y, z);

        }
    }

    ImGui::Render();
    g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
    ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

    return MyPresent(This, SyncInterval, Flags);
}

extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
WNDPROC myWNDPROC;

LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;

   
    return ::CallWindowProc(myWNDPROC,hWnd, msg, wParam, lParam);
}
HRESULT Init(
    IDXGISwapChain* This,
    /* [in] */ UINT SyncInterval,
    /* [in] */ UINT Flags) {

    myWNDPROC = (WNDPROC)SetWindowLongPtrA(hWnd, GWLP_WNDPROC, (LONG_PTR)WndProc);
    
    This->GetDevice(_uuidof(g_pd3dDevice), (void**)&g_pd3dDevice);
    g_pd3dDevice->GetImmediateContext((ID3D11DeviceContext**) &g_pd3dDeviceContext);

    ID3D11Texture2D* pBackBuffer;
    This->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);
    pBackBuffer->Release();

    ImGui::CreateContext();
    ImGui::StyleColorsDark();
    ImGui_ImplWin32_Init(hWnd);
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);

    printf("HOOK");
    // hook Present函数，当执行Present函数时，让它去执行VtPresent函数
    VirtaulTable[8] = (DWORD64)VtPresent;
    return MyPresent(This, SyncInterval, Flags);
}

DWORD Go(
    LPVOID lpThreadParameter
) {
    
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));
    sd.BufferCount = 2;
    sd.BufferDesc.Width = 0;
    sd.BufferDesc.Height = 0;
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    sd.BufferDesc.RefreshRate.Numerator = 60;
    sd.BufferDesc.RefreshRate.Denominator = 1;
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
    sd.OutputWindow = hWnd;
    sd.SampleDesc.Count = 1;
    sd.SampleDesc.Quality = 0;
    sd.Windowed = TRUE;
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;

    UINT createDeviceFlags = 0;
    //createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;
    D3D_FEATURE_LEVEL featureLevel;
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0, };
    HRESULT res = D3D11CreateDeviceAndSwapChain(nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, createDeviceFlags, featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain, &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext);
    if (res == DXGI_ERROR_UNSUPPORTED) // Try high-performance WARP software driver if hardware is not available.
        res = D3D11CreateDeviceAndSwapChain(nullptr, D3D_DRIVER_TYPE_WARP, nullptr, createDeviceFlags, featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain, &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext);
    if (res != S_OK)
        return false;

    // 得到虚表
    VirtaulTable = *(DWORD64**)g_pSwapChain;
    // 得到虚函数Present的地址
    MyPresent = (Present)VirtaulTable[8];

    DWORD a;
    // 把VirtaulTable所在的内存页修改为可读可写可执行
    VirtualProtect(VirtaulTable,1, PAGE_EXECUTE_READWRITE, &a);
    VirtaulTable[8] = (DWORD64)Init;
    return 0;
}

```

## 20. 20.UE-游戏逆向-绘制所有对象坐标

- URL: https://jisuanjiwang.blog.csdn.net/article/details/153526722
- Description: æç« æµè§éè¯»2.1kæ¬¡ï¼ç¹èµ33æ¬¡ï¼æ¶è11æ¬¡ãéè§ åæ è½¬æ¢ æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_android ue5 éåæ¾gworld

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：19.UE-游戏逆向-屏幕坐标转换 
上一个内容中找到了ProjectWorldLocationToScreen函数，在ProjectWorldLocationToScreen函数中调用了ProjectWorldToScreen函数，然后ProjectWorldLocationToScreen函数第一个参数是一个this，也就是一个APlayerController类型，如下图APlayerController从UWorld中得到 
 
接下来找APlayerController在UWorld中的偏移，所以打开之前Dump的类代码，如下图UGameInstance在0x180位置 
 
然后是UGameInstance中的 LocalPlayers，它在0x38位置，注意它是TArray类型是一个数组，需要进行加0x0取第一个数据 
 
然后进入ULocalPlayer，但是在下图红框位置看不到我们需要的PlayerController，这是因为PlayerController在父类中创建的，也就是在UPlayer类中 
 
在0x30位置，所以得到APlayerController类型的公式是(((0x180)+0x38)+0x0)+0x30 
 
然后开始写代码，首先修改下图红框的代码，添加一个& 
 
然后再写下图红框的代码，核心逻辑就是得到Aactor然后从Aactor中得到三维坐标，然后找到UE中三维坐标转屏幕坐标的函数，然后进行转换打印就可以了 
 
效果图：三维坐标转成屏幕坐标后，实现了透视 
 
完整代码

```text
// 引入主头文件（包含程序所需的基础定义、函数声明等）
#include "main.h"

// 查找UE游戏窗口：UE引擎窗口类名固定为"UnrealWindow"，获取窗口句柄（HWND）用于后续UI绘制和消息处理
HWND hWnd = FindWindowA("UnrealWindow", NULL);

// DirectX 11渲染相关组件（用于在游戏画面上叠加UI）
static ID3D11Device* g_pd3dDevice = nullptr;               // DX11设备：负责创建渲染资源（如纹理、缓冲区）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // DX11设备上下文：负责执行渲染命令（如绘制UI）
static IDXGISwapChain* g_pSwapChain = nullptr;              // 交换链：连接显卡与窗口，负责将渲染结果显示到屏幕
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 渲染目标视图：UI绘制的"画布"，最终会被交换链显示
static DWORD64* VirtaulTable;  // 交换链的虚函数表：存储DirectX函数地址，Hook通过修改这里实现

// GWorld：游戏世界（UWorld类）的全局指针地址
// 解析：游戏主程序模块基地址（通过GetModuleHandle获取） + 0x4BDAAC0（UWorld在模块中的偏移）
// UWorld是UE的核心类，管理整个游戏世界（包含关卡、玩家、实体等所有核心数据）
DWORD64 GWorld = (DWORD64)GetModuleHandleA("xxx-Win64-Shipping.exe") + 0x4BDAAC0;

// FVector：UE中表示3D空间坐标的结构体（如角色在地图中的X/Y/Z位置）
struct FVector
{
    float X;  // X轴坐标（左右方向）
    float Y;  // Y轴坐标（前后方向）
    float Z;  // Z轴坐标（上下方向）
};

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：19.UE-游戏逆向-屏幕坐标转换 
上一个内容中找到了ProjectWorldLocationToScreen函数，在ProjectWorldLocationToScreen函数中调用了ProjectWorldToScreen函数，然后ProjectWorldLocationToScreen函数第一个参数是一个this，也就是一个APlayerController类型，如下图APlayerController从UWorld中得到 
 
接下来找APlayerController在UWorld中的偏移，所以打开之前Dump的类代码，如下图UGameInstance在0x180位置 
 
然后是UGameInstance中的 LocalPlayers，它在0x38位置，注意它是TArray类型是一个数组，需要进行加0x0取第一个数据 
 
然后进入ULocalPlayer，但是在下图红框位置看不到我们需要的PlayerController，这是因为PlayerController在父类中创建的，也就是在UPlayer类中 
 
在0x30位置，所以得到APlayerController类型的公式是(((0x180)+0x38)+0x0)+0x30 
 
然后开始写代码，首先修改下图红框的代码，添加一个& 
 
然后再写下图红框的代码，核心逻辑就是得到Aactor然后从Aactor中得到三维坐标，然后找到UE中三维坐标转屏幕坐标的函数，然后进行转换打印就可以了 
 
效果图：三维坐标转成屏幕坐标后，实现了透视 
 
完整代码 

```text
// 引入主头文件（包含程序所需的基础定义、函数声明等）
#include "main.h"

// 查找UE游戏窗口：UE引擎窗口类名固定为"UnrealWindow"，获取窗口句柄（HWND）用于后续UI绘制和消息处理
HWND hWnd = FindWindowA("UnrealWindow", NULL);

// DirectX 11渲染相关组件（用于在游戏画面上叠加UI）
static ID3D11Device* g_pd3dDevice = nullptr;               // DX11设备：负责创建渲染资源（如纹理、缓冲区）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // DX11设备上下文：负责执行渲染命令（如绘制UI）
static IDXGISwapChain* g_pSwapChain = nullptr;              // 交换链：连接显卡与窗口，负责将渲染结果显示到屏幕
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 渲染目标视图：UI绘制的"画布"，最终会被交换链显示
static DWORD64* VirtaulTable;  // 交换链的虚函数表：存储DirectX函数地址，Hook通过修改这里实现

// GWorld：游戏世界（UWorld类）的全局指针地址
// 解析：游戏主程序模块基地址（通过GetModuleHandle获取） + 0x4BDAAC0（UWorld在模块中的偏移）
// UWorld是UE的核心类，管理整个游戏世界（包含关卡、玩家、实体等所有核心数据）
DWORD64 GWorld = (DWORD64)GetModuleHandleA("xxx-Win64-Shipping.exe") + 0x4BDAAC0;

// FVector：UE中表示3D空间坐标的结构体（如角色在地图中的X/Y/Z位置）
struct FVector
{
    float X;  // X轴坐标（左右方向）
    float Y;  // Y轴坐标（前后方向）
    float Z;  // Z轴坐标（上下方向）
};

// FVector2D：UE中表示2D屏幕坐标的结构体（如UI元素在屏幕上的位置）
struct FVector2D
{
    float X;  // 屏幕水平坐标（左→右）
    float Y;  // 屏幕垂直坐标（上→下）
};

// 函数指针：UE内置的"3D世界坐标转2D屏幕坐标"函数（ProjectWorldToScreen）
// 功能：将游戏中3D位置（如角色位置）转换为玩家视角下的屏幕2D位置（用于在屏幕对应位置画标签）
// 参数：Player（玩家控制器指针，提供视角基准）、WorldLocation（3D世界坐标）、ScreenLocation（输出的2D屏幕坐标）、是否相对玩家视口
typedef bool (WINAPI* FN_ProjectWorldToScreen)(void* Player, FVector& WorldLocation, FVector2D& ScreenLocation, bool bPlayerViewportRelative);

// DirectX交换链的ResizeBuffers函数指针：处理窗口大小变化时的渲染资源调整
// 当游戏窗口缩放时，需要重新创建渲染目标，否则UI会显示异常
typedef HRESULT(STDMETHODCALLTYPE* ResizeBuffers)(
    IDXGISwapChain* This,       // 交换链自身指针
    UINT BufferCount,           // 缓冲数量（画面缓存的个数）
    UINT Width,                 // 窗口新宽度
    UINT Height,                // 窗口新高度
    DXGI_FORMAT NewFormat,      // 新的像素格式（如RGBA8）
    UINT SwapChainFlags);       // 交换链标志（额外配置）
ResizeBuffers MyResizeBuffers;  // 保存原始的ResizeBuffers函数（后续需要调用以保证窗口正常缩放）

// DirectX交换链的Present函数指针：渲染流程的最后一步，负责将画面显示到屏幕
// 我们通过Hook这个函数，在游戏显示画面时插入自己的UI绘制逻辑
typedef HRESULT(STDMETHODCALLTYPE* Present)(
    IDXGISwapChain* This,       // 交换链自身指针
    UINT SyncInterval,          // 同步间隔（0表示立即显示，不等待显示器刷新）
    UINT Flags);                // 显示标志（无特殊需求填0）
Present MyPresent;  // 保存原始的Present函数（最后需要调用它让游戏画面正常显示）

// 自定义的Present钩子函数：游戏每次调用Present显示画面时，会先执行这里的逻辑
HRESULT VtPresent(
    IDXGISwapChain* This,
    UINT SyncInterval,
    UINT Flags) {

    // 初始化ImGui（轻量级UI库）的新帧：准备绘制新的UI内容（类似"准备一张透明贴纸"）
    ImGui_ImplDX11_NewFrame();
    ImGui_ImplWin32_NewFrame();
    ImGui::NewFrame();

    // 创建一个ImGui窗口（标题为"Hello, world!"，用于显示调试信息）
    ImGui::Begin("Hello, world!");

    // 步骤1：获取游戏中所有Actor（实体，如角色、道具、NPC等）的列表地址
    // 内存偏移解析：
    // GWorld（UWorld*）-> 0x30：UWorld类的CurrentLevel成员（ULevel*类型，指向当前加载的关卡）
    // -> 解引用（*）得到ULevel的地址 -> 0x98：ULevel类的Actors成员（TArray<AActor*>类型，存储关卡中所有实体）的Data指针（数组首地址）
    // -> 解引用得到Actors数组的首地址（Aactor变量，即所有实体的指针列表）
    DWORD64 Aactor = *(DWORD64*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0x98);

    // 步骤2：获取Actor列表的元素数量（即关卡中有多少个实体）
    // 内存偏移解析：
    // 同上，ULevel的Actors成员（TArray）的Num成员（元素数量）偏移为0xA0
    int Num = *(int*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0xa0);

    // 步骤3：获取"3D坐标转2D屏幕坐标"的函数地址（游戏内置函数，通过模块基地址+偏移定位）
    FN_ProjectWorldToScreen My_ProjectWorldLocationToScreen = (FN_ProjectWorldToScreen)((DWORD64)GetModuleHandleA("xxxx-Win64-Shipping.exe") + 0x2BB56F0);
    
    // 步骤4：获取玩家控制器（APlayerController）：相当于"玩家的眼睛"，用于计算坐标时以玩家视角为基准
    // 内存偏移解析：
    // GWorld（UWorld*）-> 0x180：UWorld类的PlayerControllers成员（TArray<APlayerController*>类型，存储所有玩家控制器）
    // -> 解引用得到TArray的地址 -> 0x38：TArray的Data成员（指向玩家控制器数组的首地址）
    // -> 解引用得到玩家控制器数组的首地址 -> 0x0：数组中第一个元素的偏移（即第一个玩家控制器的指针，通常是本地玩家）
    // -> 解引用得到第一个APlayerController的地址 -> 0x30：APlayerController自身实例的指针（用于后续坐标转换）
    void* Player = (void*)*(DWORD64*)(*(DWORD64*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x180) + 0x38) + 0x0) + 0x30);
    
    // 遍历所有Actor（逐个处理每个实体）
    for (int i = 0; i < Num; i++)
    {
        // 过滤无效实体：
        // 1. Aactor + 8*i：第i个Actor的指针地址（每个指针占8字节）
        // 2. *(DWORD64*)(Aactor + 8*i) != 0：指针不为空（实体存在）
        // 3. *(DWORD64*)(*(DWORD64*)(Aactor + 8*i) + 0x130) != 0：实体的根组件存在（根组件存储位置信息）
        // 其中0x130是AActor类的RootComponent成员（USceneComponent*类型，实体的根组件，必含位置数据）
        if ((Aactor + 8 * i) != 0 && *(DWORD64*)(Aactor + 8 * i) != 0 && *(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) != 0) {
            
            // 步骤5：获取当前Actor的3D世界坐标（从根组件中读取）
            FVector MyFVector = { 0,0,0 };  // 初始化3D坐标
            // 解析：
            // 根组件（USceneComponent*）的RelativeLocation成员（FVector类型，存储实体的位置）
            // 0x1D0：RelativeLocation.X（X轴坐标）
            // 0x1D4：RelativeLocation.Y（Y轴坐标）
            // 0x1D8：RelativeLocation.Z（Z轴坐标）
            MyFVector.X = *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) + 0x1d0);
            MyFVector.Y = *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) + 0x1d4);
            MyFVector.Z = *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) + 0x1d8);

            // 步骤6：将3D世界坐标转换为屏幕2D坐标（使用玩家控制器的视角）
            FVector2D MyFVector2D = { 0,0 };  // 初始化2D坐标
            My_ProjectWorldLocationToScreen(Player, MyFVector, MyFVector2D, 1);  // 最后一个参数1表示坐标相对玩家视口

            // 步骤7：在屏幕对应位置绘制黄色文本"AM"（标记该实体）
            ImGui::GetForegroundDrawList()->AddText({ MyFVector2D.X,MyFVector2D.Y }, ImColor(255, 255, 0), "AM");
        }
    }
    
    // 结束ImGui窗口绘制（完成当前帧UI绘制）
    ImGui::End();

    // 将ImGui绘制的UI内容渲染到屏幕（把"贴纸"贴到游戏画面上）
    ImGui::Render();
    g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);  // 设置渲染目标
    ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());  // 渲染UI数据

    // 调用原始的Present函数，让游戏画面正常显示（保留游戏原本的画面）
    return MyPresent(This, SyncInterval, Flags);
}

// ImGui的窗口消息处理函数：用于处理UI的输入事件（如鼠标点击、键盘输入）
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
WNDPROC myWNDPROC;  // 保存原始的窗口消息处理函数（用于后续还原消息处理）

// 自定义的窗口消息钩子：拦截窗口消息，让ImGui能响应输入（如拖动UI窗口、输入文字）
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    // 让ImGui先处理消息（如果是UI相关事件，如点击ImGui窗口，则由ImGui处理）
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;

    // 非UI事件，调用原始的窗口消息处理函数（保证游戏本身的操作正常，如移动、跳跃）
    return ::CallWindowProc(myWNDPROC, hWnd, msg, wParam, lParam);
}

// 初始化函数：第一次调用Present时执行，用于设置ImGui和完成Hook
HRESULT Init(
    IDXGISwapChain* This,
    UINT SyncInterval,
    UINT Flags) {

    // 从交换链获取DirectX设备和设备上下文（用于后续创建UI渲染资源）
    This->GetDevice(_uuidof(g_pd3dDevice), (void**)&g_pd3dDevice);
    g_pd3dDevice->GetImmediateContext((ID3D11DeviceContext**)&g_pd3dDeviceContext);

    // 创建渲染目标视图（UI绘制的"画布"，关联到游戏窗口的后台缓冲）
    ID3D11Texture2D* pBackBuffer;  // 后台缓冲（游戏画面的原始数据存储在这里）
    This->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));  // 获取交换链的第一个缓冲
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);  // 创建渲染目标
    pBackBuffer->Release();  // 释放临时缓冲（已通过渲染目标关联）

    // 初始化ImGui（仅执行一次，避免重复初始化）
    static bool is = true;
    if (is) {
        is = false;
        // Hook窗口消息处理函数（让ImGui能接收鼠标/键盘输入）
        myWNDPROC = (WNDPROC)SetWindowLongPtrA(hWnd, GWLP_WNDPROC, (LONG_PTR)WndProc);
        ImGui::CreateContext();  // 创建ImGui上下文（核心数据结构）
        ImGui::StyleColorsDark();  // 设置UI主题为深色
        ImGui_ImplWin32_Init(hWnd);  // 初始化ImGui的Win32平台支持（关联窗口）
    }

    // 初始化ImGui的DirectX 11支持（关联DX设备和上下文，用于绘制UI）
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);

    printf("HOOK成功");  // 打印日志，提示Hook已完成

    // 将交换链虚函数表中的Present函数地址替换为自定义的VtPresent（完成Hook）
    // 后续游戏调用Present时，会先执行VtPresent中的逻辑（即我们的UI绘制）
    VirtaulTable[8] = (DWORD64)VtPresent;
    return MyPresent(This, SyncInterval, Flags);  // 调用原始Present，显示第一帧画面
}

// 窗口大小变化钩子：处理窗口缩放时的资源释放（避免UI渲染错误）
HRESULT VtResizeBuffers(
    IDXGISwapChain* This,
    UINT BufferCount,
    UINT Width,
    UINT Height,
    DXGI_FORMAT NewFormat,
    UINT SwapChainFlags) {

    // 窗口大小变化时，释放ImGui和DirectX的相关资源（旧资源尺寸不匹配新窗口）
    if (g_pd3dDevice) {
        g_pd3dDevice->Release();  // 释放DX设备
        g_pd3dDevice = nullptr;
        g_mainRenderTargetView->Release();  // 释放旧渲染目标
        ImGui_ImplDX11_Shutdown();  // 关闭ImGui的DX支持
        VirtaulTable[8] = (DWORD64)Init;  // 暂时恢复Present为Init，下次调用时重新初始化资源
    }

    // 调用原始的ResizeBuffers函数，让游戏正常处理窗口大小变化（调整自身渲染资源）
    return MyResizeBuffers(This, BufferCount, Width, Height, NewFormat, SwapChainFlags);
}

// 线程入口函数：负责初始化DirectX环境并完成Hook
DWORD Go(LPVOID lpThreadParameter) {
    // 初始化交换链描述（定义DirectX交换链的配置，如缓冲数量、像素格式、关联窗口等）
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));  // 清空结构体，避免随机值影响配置
    sd.BufferCount = 2;  // 双缓冲（减少画面闪烁）
    sd.BufferDesc.Width = 0;  // 宽度随窗口自动调整
    sd.BufferDesc.Height = 0;  // 高度随窗口自动调整
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;  // 像素格式：RGBA各8位（标准彩色）
    sd.BufferDesc.RefreshRate.Numerator = 60;  // 刷新率60Hz
    sd.BufferDesc.RefreshRate.Denominator = 1;
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;  // 允许切换显示模式（如全屏/窗口）
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;  // 缓冲用途：渲染目标输出（存储画面）
    sd.OutputWindow = hWnd;  // 关联到游戏窗口
    sd.SampleDesc.Count = 1;  // 采样数1（不开启抗锯齿）
    sd.SampleDesc.Quality = 0;
    sd.Windowed = TRUE;  // 窗口模式（非全屏）
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;  // 交换后丢弃旧缓冲（提高性能）

    // 创建DirectX 11设备和交换链（用于后续Hook渲染函数）
    UINT createDeviceFlags = 0;  // 设备创建标志（无特殊需求填0）
    D3D_FEATURE_LEVEL featureLevel;  // 支持的DX特性等级
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0, };  // 优先DX11， fallback到DX10
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, createDeviceFlags,
        featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain,
        &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext
    );
    // 如果硬件不支持DX11，尝试使用软件模拟驱动（WARP）
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP, nullptr, createDeviceFlags,
            featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain,
            &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext
        );
    if (res != S_OK)  // 创建失败则退出线程
        return false;

    // 获取交换链的虚函数表（DirectX函数通过虚表调用，修改虚表实现Hook）
    VirtaulTable = *(DWORD64**)g_pSwapChain;  // 虚函数表是交换链的第一个成员（偏移0x0）
    MyPresent = (Present)VirtaulTable[8];  // 保存原始Present函数（虚表中索引8是Present）

    // 修改虚函数表的内存保护属性（默认只读，需改为可写才能修改函数地址）
    DWORD a;  // 用于接收旧的保护属性
    VirtualProtect(VirtaulTable, 1, PAGE_EXECUTE_READWRITE, &a);  // 改为可读可写可执行
    VirtaulTable[8] = (DWORD64)Init;  // 将Present函数地址替换为Init（第一次调用Present时执行初始化）

    // 同理Hook ResizeBuffers函数（虚表中索引13是ResizeBuffers）
    MyResizeBuffers = (ResizeBuffers)VirtaulTable[13];  // 保存原始ResizeBuffers
    VirtaulTable[13] = (DWORD64)VtResizeBuffers;  // 替换为自定义的VtResizeBuffers

    return 0;  // 线程执行完成
}

```

## 21. 21.UE-游戏逆向-绘制解密对象名字

- URL: https://jisuanjiwang.blog.csdn.net/article/details/153575840
- Description: æç« æµè§éè¯»1.1kæ¬¡ï¼ç¹èµ13æ¬¡ï¼æ¶è2æ¬¡ãèå¹» èå¹»å¼æ UE4 UnrealEngine4 æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_dma éå projectworldlocationtoscreen

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：20.UE-游戏逆向-绘制所有对象坐标 
首先把8.UE-游戏逆向-代码实现GetName算法（一）里获取GName的算法复制出来，如下图复制到dll中 
 
然后使用GetName获取名字 
 
如下图红框，正常打印了名字 
 
完整代码

```text
#include "main.h"

HWND hWnd = FindWindowA("UnrealWindow", NULL);

static ID3D11Device* g_pd3dDevice = nullptr;
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;
static IDXGISwapChain* g_pSwapChain = nullptr;
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;
DWORD64* VirtaulTable;

DWORD64 GWorld = (DWORD64)GetModuleHandleA("xxxxx.exe") + 0x4B48780;

struct FVector
{
    float                                         X;                                                            // 0x0000(0x0004)
    float                                         Y;                                                            // 0x0004(0x0004)
    float                                         Z;                                                            // 0x0008(0x0004)
};

// ScriptStruct  CoreUObject.Vector2D
// Struct Size::0x0008
struct FVector2D
{
    float                                         X;                                                            // 0x0000(0x0004)
    float                                         Y;                                                            // 0x0004(0x0004)
};

typedef bool (WINAPI* FN_ProjectWorldToScreen)(void* Player, FVector& WorldLocation, FVector2D& ScreenLocation, bool bPlayerViewportRelative);

typedef HRESULT(STDMETHODCALLTYPE* ResizeBuffers)(
    IDXGISwapChain* This,
    /* [in] */ UINT BufferCount,
    /* [in] */ UINT Width,
    /* [in] */ UINT Height,
    /* [in] */ DXGI_FORMAT NewFormat,
    /* [in] */ UINT SwapChainFlags);

ResizeBuffers MyResizeBuffers;

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：20.UE-游戏逆向-绘制所有对象坐标 
首先把8.UE-游戏逆向-代码实现GetName算法（一）里获取GName的算法复制出来，如下图复制到dll中 
 
然后使用GetName获取名字 
 
如下图红框，正常打印了名字 
 
完整代码 

```text
#include "main.h"

HWND hWnd = FindWindowA("UnrealWindow", NULL);

static ID3D11Device* g_pd3dDevice = nullptr;
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;
static IDXGISwapChain* g_pSwapChain = nullptr;
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;
DWORD64* VirtaulTable;

DWORD64 GWorld = (DWORD64)GetModuleHandleA("xxxxx.exe") + 0x4B48780;

struct FVector
{
    float                                         X;                                                            // 0x0000(0x0004)
    float                                         Y;                                                            // 0x0004(0x0004)
    float                                         Z;                                                            // 0x0008(0x0004)
};

// ScriptStruct  CoreUObject.Vector2D
// Struct Size::0x0008
struct FVector2D
{
    float                                         X;                                                            // 0x0000(0x0004)
    float                                         Y;                                                            // 0x0004(0x0004)
};

typedef bool (WINAPI* FN_ProjectWorldToScreen)(void* Player, FVector& WorldLocation, FVector2D& ScreenLocation, bool bPlayerViewportRelative);

typedef HRESULT(STDMETHODCALLTYPE* ResizeBuffers)(
    IDXGISwapChain* This,
    /* [in] */ UINT BufferCount,
    /* [in] */ UINT Width,
    /* [in] */ UINT Height,
    /* [in] */ DXGI_FORMAT NewFormat,
    /* [in] */ UINT SwapChainFlags);

ResizeBuffers MyResizeBuffers;

typedef  HRESULT(STDMETHODCALLTYPE* Present)(
    IDXGISwapChain* This,
    /* [in] */ UINT SyncInterval,
    /* [in] */ UINT Flags);
Present MyPresent;

using namespace std;  // 简化代码，不用每次写"std::"

// 字符串头部信息结构体（存储字符串的基本属性）
struct FNameEntryHeader
{
    // 位域：将2字节（16位）分成多个小部分，节省内存
    uint16_t bIsWide : 1;       // 1位：是否为宽字符（1=是，可存中文；0=否，仅存英文）
    uint16_t LowercaseProbeHash : 5;  // 5位：小写哈希值（用于快速比较字符串）
    uint16_t Len : 10;               // 10位：字符串长度（最多1023个字符）
};

// 字符串数据结构体（包含头部信息和实际字符）
struct FNameEntry
{
    FNameEntryHeader Header;  // 字符串的头部信息（长度、是否宽字符等）

    // 联合体：两种字符存储方式共用一块内存（节省空间）
    union
    {
        char AnsiName[1024];    // 普通字符数组（存英文/数字，1字节/字符）
        wchar_t WideName[1024]; // 宽字符数组（存中文等，2字节/字符）
    };
};

// 游戏中"全局名字池"（GName）的地址
// GName相当于游戏的"名字字典"，所有用到的名字都存在这里，每个名字有唯一ID
// 地址说明：0x7FF76F580000（游戏程序基地址） + 0x4A56400（GName偏移） + 0x10（实际存储位置）
// 注意：这个地址是逆向游戏得到的，换游戏或更新后会变化
uint8_t* GName = (uint8_t*)(0x7FF719360000 + 0x49C40C0 + 0x10);

// 从游戏进程中读取指定地址的内存（获取GName中的"块地址"）
// 参数：a = 要读取的游戏内存地址
// 返回：读取到的"块地址"（GName中存储名字的一个区块起始位置）
uint8_t* MyReadProessMemory(uint8_t* a) {
    // 1. 找到游戏窗口（UE引擎游戏的窗口类名通常是"UnrealWindow"）
    HWND nhwnd = FindWindowA("UnrealWindow", 0);  // 0 = 不限制窗口标题

    // 2. 获取游戏进程ID（每个运行的程序都有唯一ID，类似身份证号）
    DWORD pid = 0;
    GetWindowThreadProcessId(nhwnd, &pid);  // 通过窗口句柄获取进程ID

    // 3. 打开游戏进程，获取读取内存的权限（类似拿到访问游戏内存的钥匙）
    HANDLE nhandle = OpenProcess(PROCESS_ALL_ACCESS, 0, pid);

    // 4. 读取目标地址的8字节数据（64位系统中地址占8字节）
    uint8_t* buf;  // 存储读取到的地址
    ReadProcessMemory(nhandle, a, &buf, 8, NULL);

    return (uint8_t*)buf;  // 返回读取到的"块地址"
}

// 从游戏进程中读取指定地址的FNameEntry结构体（包含字符串实际内容）
// 参数：a = FNameEntry在游戏内存中的地址
// 返回：读取到的FNameEntry结构体（包含字符串数据）
FNameEntry MyReadProessMemoryFNameEntry(FNameEntry* a) {
    // 1. 找到游戏窗口并获取进程ID（和上面步骤相同）
    HWND nhwnd = FindWindowA("UnrealWindow", 0);
    DWORD pid = 0;
    GetWindowThreadProcessId(nhwnd, &pid);

    // 2. 打开游戏进程
    HANDLE nhandle = OpenProcess(PROCESS_ALL_ACCESS, 0, pid);

    // 3. 读取整个FNameEntry结构体（包含头部和字符数据）
    FNameEntry buf;  // 存储读取到的结构体
    ReadProcessMemory(nhandle, a, &buf, sizeof(FNameEntry), NULL);

    return buf;  // 返回读取到的字符串数据
}

// 根据ID获取对应的名字（核心函数）
// 参数：id = 名字在GName中的唯一编号（0、1、2...）
// 返回：id对应的字符串（如"Player"、"Item"等）
string GetName(int id) {
    // 1. 计算GName中"块"的地址（GName按"块"存储名字，类似字典分章节）
    // id >> 16 = 取ID的高16位作为"块索引"（确定是哪一章）
    // 每个块的地址占8字节，所以乘以8定位到块在GName中的位置
    uint8_t* a = MyReadProessMemory(GName + (id >> 16) * 8);

    // 2. 计算块内偏移（确定是这一章的第几页）
    // id & 65535 = 取ID的低16位（65535 = 2^16 - 1，刚好取低16位）
    // 乘以2作为偏移量（原代码逻辑，实际应按结构体大小计算）
    uint8_t* b = (uint8_t*)(2 * (id & 65535));

    // 3. 计算具体字符串的地址并读取数据
    // a（块地址） + b（块内偏移） = 该ID对应的字符串数据地址
    FNameEntry info = MyReadProessMemoryFNameEntry((FNameEntry*)((DWORD64)a + b));

    // 4. 从结构体中提取字符串（按头部信息的长度截取）
    return string(info.AnsiName, info.Header.Len);
}

HRESULT VtPresent(
    IDXGISwapChain* This,
    /* [in] */ UINT SyncInterval,
    /* [in] */ UINT Flags) {

    ImGui_ImplDX11_NewFrame();
    ImGui_ImplWin32_NewFrame();
    ImGui::NewFrame();

    ImGui::Begin("Hello, world!");

    // 得到 Aactors
    DWORD64 Aactor = *(DWORD64*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0x98);
    // 得到Aactor里内容的数量
    int Num = *(int*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0xa0);

    FN_ProjectWorldToScreen My_ProjectWorldLocationToScreen = (FN_ProjectWorldToScreen)((DWORD64)GetModuleHandleA("xxxxx.exe") + 0x2B51EA0);
    // 取APlayerController
    void* Player = (void*)*(DWORD64*)(*(DWORD64*)(*(DWORD64*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x180) + 0x38) + 0x0) + 0x30);
    for (int i = 0; i < Num; i++)
    {
        //  *(DWORD64*)(Aactor + 8 * i) != 0意思是从Aactors里取一个数据，判断这个数据是不是存在，不等于0就存在
        if ((Aactor + 8 * i) != 0 && *(DWORD64*)(Aactor + 8 * i) != 0 && *(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) != 0) {
            // (*(DWORD64*)(Aactor + 8 * i) + 0x130)取出 RootComponent根组件
            // *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130)+0x1d0); 取出x坐标
            FVector MyFVector = { 0,0,0 };

            MyFVector.X = *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) + 0x1d0);
            MyFVector.Y = *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) + 0x1d4);

            MyFVector.Z = *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) + 0x1d8);

            FVector2D MyFVector2D = { 0,0 };
            My_ProjectWorldLocationToScreen(Player, MyFVector, MyFVector2D, 1);
            ImGui::GetForegroundDrawList()->AddText({ MyFVector2D.X,MyFVector2D.Y }, ImColor(255, 255, 0), GetName(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x18)).c_str());

        }
    }
    ImGui::End();

    ImGui::Render();
    g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
    ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

    return MyPresent(This, SyncInterval, Flags);
}

extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
WNDPROC myWNDPROC;

LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;

    return ::CallWindowProc(myWNDPROC, hWnd, msg, wParam, lParam);
}
HRESULT Init(
    IDXGISwapChain* This,
    /* [in] */ UINT SyncInterval,
    /* [in] */ UINT Flags) {

    This->GetDevice(_uuidof(g_pd3dDevice), (void**)&g_pd3dDevice);
    g_pd3dDevice->GetImmediateContext((ID3D11DeviceContext**)&g_pd3dDeviceContext);

    ID3D11Texture2D* pBackBuffer;
    This->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));

    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);
    pBackBuffer->Release();

    static bool is = true;
    if (is) {
        is = false;
        myWNDPROC = (WNDPROC)SetWindowLongPtrA(hWnd, GWLP_WNDPROC, (LONG_PTR)WndProc);
        ImGui::CreateContext();
        ImGui::StyleColorsDark();
        ImGui_ImplWin32_Init(hWnd);
    }

    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);

    printf("HOOK");
    // hook Present函数，当执行Present函数时，让它去执行VtPresent函数
    VirtaulTable[8] = (DWORD64)VtPresent;
    return MyPresent(This, SyncInterval, Flags);
}

HRESULT VtResizeBuffers(
    IDXGISwapChain* This,
    /* [in] */ UINT BufferCount,
    /* [in] */ UINT Width,
    /* [in] */ UINT Height,
    /* [in] */ DXGI_FORMAT NewFormat,
    /* [in] */ UINT SwapChainFlags) {

    // 释放我们自己创建的资源
    if (g_pd3dDevice) {
        g_pd3dDevice->Release();
        g_pd3dDevice = nullptr;
        g_mainRenderTargetView->Release();
        ImGui_ImplDX11_Shutdown();
        VirtaulTable[8] = (DWORD64)Init;
    }

    // 调用原本的逻辑，释放资源
    return MyResizeBuffers(This, BufferCount, Width, Height, NewFormat, SwapChainFlags);
}

DWORD Go(
    LPVOID lpThreadParameter
) {
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));
    sd.BufferCount = 2;
    sd.BufferDesc.Width = 0;
    sd.BufferDesc.Height = 0;
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    sd.BufferDesc.RefreshRate.Numerator = 60;
    sd.BufferDesc.RefreshRate.Denominator = 1;
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
    sd.OutputWindow = hWnd;
    sd.SampleDesc.Count = 1;
    sd.SampleDesc.Quality = 0;
    sd.Windowed = TRUE;
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;

    UINT createDeviceFlags = 0;
    //createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;
    D3D_FEATURE_LEVEL featureLevel;
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0, };
    HRESULT res = D3D11CreateDeviceAndSwapChain(nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, createDeviceFlags, featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain, &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext);
    if (res == DXGI_ERROR_UNSUPPORTED) // Try high-performance WARP software driver if hardware is not available.
        res = D3D11CreateDeviceAndSwapChain(nullptr, D3D_DRIVER_TYPE_WARP, nullptr, createDeviceFlags, featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain, &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext);
    if (res != S_OK)
        return false;

    // 得到虚表
    VirtaulTable = *(DWORD64**)g_pSwapChain;
    // 得到虚函数Present的地址
    MyPresent = (Present)VirtaulTable[8];

    DWORD a;
    // 把VirtaulTable所在的内存页修改为可读可写可执行
    VirtualProtect(VirtaulTable, 1, PAGE_EXECUTE_READWRITE, &a);
    VirtaulTable[8] = (DWORD64)Init;

    MyResizeBuffers = (ResizeBuffers)VirtaulTable[13];
    VirtaulTable[13] = (DWORD64)VtResizeBuffers;
    return 0;
}

```

## 22. 22.UE-游戏逆向-只绘制敌人

- URL: https://jisuanjiwang.blog.csdn.net/article/details/153644093
- Description: æç« æµè§éè¯»1.4kæ¬¡ï¼ç¹èµ8æ¬¡ï¼æ¶è4æ¬¡ãèå¹»å¼æ èå¹» UE4 UnrealEngine4 æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_ue4 projectworldlocationtoscreen

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：21.UE-游戏逆向-绘制解密对象名字 
效果图： 
 
就添加了下图红框的代码，就是判断当前Aactor的名字是不是怪物的名字，怪物的名字都是以Zombie_BP开头的 
 
完整代码：

```text
#include "main.h"

HWND hWnd = FindWindowA("UnrealWindow", NULL);

static ID3D11Device* g_pd3dDevice = nullptr;
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;
static IDXGISwapChain* g_pSwapChain = nullptr;
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;
DWORD64* VirtaulTable;

DWORD64 add = (DWORD64)GetModuleHandleA("xxx.exe");
DWORD64 GWorld = add + 0x4B48780;
struct FVector
{
    float                                         X;                                                            // 0x0000(0x0004)
    float                                         Y;                                                            // 0x0004(0x0004)
    float                                         Z;                                                            // 0x0008(0x0004)
};

// ScriptStruct  CoreUObject.Vector2D
// Struct Size::0x0008
struct FVector2D
{
    float                                         X;                                                            // 0x0000(0x0004)
    float                                         Y;                                                            // 0x0004(0x0004)
};

typedef bool (WINAPI* FN_ProjectWorldToScreen)(void* Player, FVector& WorldLocation, FVector2D& ScreenLocation, bool bPlayerViewportRelative);

typedef HRESULT(STDMETHODCALLTYPE* ResizeBuffers)(
    IDXGISwapChain* This,
    /* [in] */ UINT BufferCount,
    /* [in] */ UINT Width,
    /* [in] */ UINT Height,
    /* [in] */ DXGI_FORMAT NewFormat,
    /* [in] */ UINT SwapChainFlags);

ResizeBuffers MyResizeBuffers;

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：21.UE-游戏逆向-绘制解密对象名字 
效果图： 
 
就添加了下图红框的代码，就是判断当前Aactor的名字是不是怪物的名字，怪物的名字都是以Zombie_BP开头的 
 
完整代码： 

```text
#include "main.h"

HWND hWnd = FindWindowA("UnrealWindow", NULL);

static ID3D11Device* g_pd3dDevice = nullptr;
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;
static IDXGISwapChain* g_pSwapChain = nullptr;
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;
DWORD64* VirtaulTable;

DWORD64 add = (DWORD64)GetModuleHandleA("xxx.exe");
DWORD64 GWorld = add + 0x4B48780;
struct FVector
{
    float                                         X;                                                            // 0x0000(0x0004)
    float                                         Y;                                                            // 0x0004(0x0004)
    float                                         Z;                                                            // 0x0008(0x0004)
};

// ScriptStruct  CoreUObject.Vector2D
// Struct Size::0x0008
struct FVector2D
{
    float                                         X;                                                            // 0x0000(0x0004)
    float                                         Y;                                                            // 0x0004(0x0004)
};

typedef bool (WINAPI* FN_ProjectWorldToScreen)(void* Player, FVector& WorldLocation, FVector2D& ScreenLocation, bool bPlayerViewportRelative);

typedef HRESULT(STDMETHODCALLTYPE* ResizeBuffers)(
    IDXGISwapChain* This,
    /* [in] */ UINT BufferCount,
    /* [in] */ UINT Width,
    /* [in] */ UINT Height,
    /* [in] */ DXGI_FORMAT NewFormat,
    /* [in] */ UINT SwapChainFlags);

ResizeBuffers MyResizeBuffers;

typedef  HRESULT(STDMETHODCALLTYPE* Present)(
    IDXGISwapChain* This,
    /* [in] */ UINT SyncInterval,
    /* [in] */ UINT Flags);
Present MyPresent;

using namespace std;  // 简化代码，不用每次写"std::"

// 字符串头部信息结构体（存储字符串的基本属性）
struct FNameEntryHeader
{
    // 位域：将2字节（16位）分成多个小部分，节省内存
    uint16_t bIsWide : 1;       // 1位：是否为宽字符（1=是，可存中文；0=否，仅存英文）
    uint16_t LowercaseProbeHash : 5;  // 5位：小写哈希值（用于快速比较字符串）
    uint16_t Len : 10;               // 10位：字符串长度（最多1023个字符）
};

// 字符串数据结构体（包含头部信息和实际字符）
struct FNameEntry
{
    FNameEntryHeader Header;  // 字符串的头部信息（长度、是否宽字符等）

    // 联合体：两种字符存储方式共用一块内存（节省空间）
    union
    {
        char AnsiName[1024];    // 普通字符数组（存英文/数字，1字节/字符）
        wchar_t WideName[1024]; // 宽字符数组（存中文等，2字节/字符）
    };
};

// 游戏中"全局名字池"（GName）的地址
// GName相当于游戏的"名字字典"，所有用到的名字都存在这里，每个名字有唯一ID
// 地址说明：0x7FF76F580000（游戏程序基地址） + 0x4A56400（GName偏移） + 0x10（实际存储位置）
// 注意：这个地址是逆向游戏得到的，换游戏或更新后会变化
uint8_t* GName = (uint8_t*)(add + 0x49C40C0 + 0x10);

// 从游戏进程中读取指定地址的内存（获取GName中的"块地址"）
// 参数：a = 要读取的游戏内存地址
// 返回：读取到的"块地址"（GName中存储名字的一个区块起始位置）
uint8_t* MyReadProessMemory(uint8_t* a) {
    // 1. 找到游戏窗口（UE引擎游戏的窗口类名通常是"UnrealWindow"）
    HWND nhwnd = FindWindowA("UnrealWindow", 0);  // 0 = 不限制窗口标题

    // 2. 获取游戏进程ID（每个运行的程序都有唯一ID，类似身份证号）
    DWORD pid = 0;
    GetWindowThreadProcessId(nhwnd, &pid);  // 通过窗口句柄获取进程ID

    // 3. 打开游戏进程，获取读取内存的权限（类似拿到访问游戏内存的钥匙）
    HANDLE nhandle = OpenProcess(PROCESS_ALL_ACCESS, 0, pid);

    // 4. 读取目标地址的8字节数据（64位系统中地址占8字节）
    uint8_t* buf;  // 存储读取到的地址
    ReadProcessMemory(nhandle, a, &buf, 8, NULL);

    return (uint8_t*)buf;  // 返回读取到的"块地址"
}

// 从游戏进程中读取指定地址的FNameEntry结构体（包含字符串实际内容）
// 参数：a = FNameEntry在游戏内存中的地址
// 返回：读取到的FNameEntry结构体（包含字符串数据）
FNameEntry MyReadProessMemoryFNameEntry(FNameEntry* a) {
    // 1. 找到游戏窗口并获取进程ID（和上面步骤相同）
    HWND nhwnd = FindWindowA("UnrealWindow", 0);
    DWORD pid = 0;
    GetWindowThreadProcessId(nhwnd, &pid);

    // 2. 打开游戏进程
    HANDLE nhandle = OpenProcess(PROCESS_ALL_ACCESS, 0, pid);

    // 3. 读取整个FNameEntry结构体（包含头部和字符数据）
    FNameEntry buf;  // 存储读取到的结构体
    ReadProcessMemory(nhandle, a, &buf, sizeof(FNameEntry), NULL);

    return buf;  // 返回读取到的字符串数据
}

// 根据ID获取对应的名字（核心函数）
// 参数：id = 名字在GName中的唯一编号（0、1、2...）
// 返回：id对应的字符串（如"Player"、"Item"等）
string GetName(int id) {
    // 1. 计算GName中"块"的地址（GName按"块"存储名字，类似字典分章节）
    // id >> 16 = 取ID的高16位作为"块索引"（确定是哪一章）
    // 每个块的地址占8字节，所以乘以8定位到块在GName中的位置
    uint8_t* a = MyReadProessMemory(GName + (id >> 16) * 8);

    // 2. 计算块内偏移（确定是这一章的第几页）
    // id & 65535 = 取ID的低16位（65535 = 2^16 - 1，刚好取低16位）
    // 乘以2作为偏移量（原代码逻辑，实际应按结构体大小计算）
    uint8_t* b = (uint8_t*)(2 * (id & 65535));

    // 3. 计算具体字符串的地址并读取数据
    // a（块地址） + b（块内偏移） = 该ID对应的字符串数据地址
    FNameEntry info = MyReadProessMemoryFNameEntry((FNameEntry*)((DWORD64)a + b));

    // 4. 从结构体中提取字符串（按头部信息的长度截取）
    return string(info.AnsiName, info.Header.Len);
}

HRESULT VtPresent(
    IDXGISwapChain* This,
    /* [in] */ UINT SyncInterval,
    /* [in] */ UINT Flags) {

    ImGui_ImplDX11_NewFrame();
    ImGui_ImplWin32_NewFrame();
    ImGui::NewFrame();

    ImGui::Begin("Hello, world!");

    // 得到 Aactors
    DWORD64 Aactor = *(DWORD64*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0x98);
    // 得到Aactor里内容的数量
    int Num = *(int*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0xa0);

    FN_ProjectWorldToScreen My_ProjectWorldLocationToScreen = (FN_ProjectWorldToScreen)(add + 0x2B51EA0);
    // 取APlayerController
    void* Player = (void*)*(DWORD64*)(*(DWORD64*)(*(DWORD64*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x180) + 0x38) + 0x0) + 0x30);
    for (int i = 0; i < Num; i++)
    {
     

        //  *(DWORD64*)(Aactor + 8 * i) != 0意思是从Aactors里取一个数据，判断这个数据是不是存在，不等于0就存在
        if ((Aactor + 8 * i) != 0 && *(DWORD64*)(Aactor + 8 * i) != 0 && *(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) != 0) {
            string name = GetName(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x18));
            if (name.find("Zombie_BP") == string::npos)
                continue;
            // (*(DWORD64*)(Aactor + 8 * i) + 0x130)取出 RootComponent根组件
            // *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130)+0x1d0); 取出x坐标
            FVector MyFVector = { 0,0,0 };

            MyFVector.X = *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) + 0x1d0);
            MyFVector.Y = *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) + 0x1d4);

            MyFVector.Z = *(float*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) + 0x1d8);

            FVector2D MyFVector2D = { 0,0 };
            My_ProjectWorldLocationToScreen(Player, MyFVector, MyFVector2D, 1);
            ImGui::GetForegroundDrawList()->AddText({ MyFVector2D.X,MyFVector2D.Y }, ImColor(255, 255, 0), name.c_str());

        }
    }
    ImGui::End();

    ImGui::Render();
    g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
    ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

    return MyPresent(This, SyncInterval, Flags);
}

extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
WNDPROC myWNDPROC;

LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;

    return ::CallWindowProc(myWNDPROC, hWnd, msg, wParam, lParam);
}
HRESULT Init(
    IDXGISwapChain* This,
    /* [in] */ UINT SyncInterval,
    /* [in] */ UINT Flags) {

    This->GetDevice(_uuidof(g_pd3dDevice), (void**)&g_pd3dDevice);
    g_pd3dDevice->GetImmediateContext((ID3D11DeviceContext**)&g_pd3dDeviceContext);

    ID3D11Texture2D* pBackBuffer;
    This->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));

    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);
    pBackBuffer->Release();

    static bool is = true;
    if (is) {
        is = false;
        myWNDPROC = (WNDPROC)SetWindowLongPtrA(hWnd, GWLP_WNDPROC, (LONG_PTR)WndProc);
        ImGui::CreateContext();
        ImGui::StyleColorsDark();
        ImGui_ImplWin32_Init(hWnd);
    }

    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);

    printf("HOOK");
    // hook Present函数，当执行Present函数时，让它去执行VtPresent函数
    VirtaulTable[8] = (DWORD64)VtPresent;
    return MyPresent(This, SyncInterval, Flags);
}

HRESULT VtResizeBuffers(
    IDXGISwapChain* This,
    /* [in] */ UINT BufferCount,
    /* [in] */ UINT Width,
    /* [in] */ UINT Height,
    /* [in] */ DXGI_FORMAT NewFormat,
    /* [in] */ UINT SwapChainFlags) {

    // 释放我们自己创建的资源
    if (g_pd3dDevice) {
        g_pd3dDevice->Release();
        g_pd3dDevice = nullptr;
        g_mainRenderTargetView->Release();
        ImGui_ImplDX11_Shutdown();
        VirtaulTable[8] = (DWORD64)Init;
    }

    // 调用原本的逻辑，释放资源
    return MyResizeBuffers(This, BufferCount, Width, Height, NewFormat, SwapChainFlags);
}

DWORD Go(
    LPVOID lpThreadParameter
) {
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));
    sd.BufferCount = 2;
    sd.BufferDesc.Width = 0;
    sd.BufferDesc.Height = 0;
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    sd.BufferDesc.RefreshRate.Numerator = 60;
    sd.BufferDesc.RefreshRate.Denominator = 1;
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
    sd.OutputWindow = hWnd;
    sd.SampleDesc.Count = 1;
    sd.SampleDesc.Quality = 0;
    sd.Windowed = TRUE;
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;

    UINT createDeviceFlags = 0;
    //createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;
    D3D_FEATURE_LEVEL featureLevel;
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0, };
    HRESULT res = D3D11CreateDeviceAndSwapChain(nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, createDeviceFlags, featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain, &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext);
    if (res == DXGI_ERROR_UNSUPPORTED) // Try high-performance WARP software driver if hardware is not available.
        res = D3D11CreateDeviceAndSwapChain(nullptr, D3D_DRIVER_TYPE_WARP, nullptr, createDeviceFlags, featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain, &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext);
    if (res != S_OK)
        return false;

    // 得到虚表
    VirtaulTable = *(DWORD64**)g_pSwapChain;
    // 得到虚函数Present的地址
    MyPresent = (Present)VirtaulTable[8];

    DWORD a;
    // 把VirtaulTable所在的内存页修改为可读可写可执行
    VirtualProtect(VirtaulTable, 1, PAGE_EXECUTE_READWRITE, &a);
    VirtaulTable[8] = (DWORD64)Init;

    MyResizeBuffers = (ResizeBuffers)VirtaulTable[13];
    VirtaulTable[13] = (DWORD64)VtResizeBuffers;
    return 0;
}

```

## 23. 23.UE-游戏逆向-寻找骨骼坐标

- URL: https://jisuanjiwang.blog.csdn.net/article/details/153697695
- Description: æç« æµè§éè¯»1.1kæ¬¡ï¼ç¹èµ8æ¬¡ï¼æ¶è10æ¬¡ãèå¹»å¼æ UE4 UnrealEngine4 æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_éåå·¥ç¨æ­£å¸¸çéª¨éª¼å¨åå­ä¸­çæ ·å­

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：22.UE-游戏逆向-只绘制敌人 
骨骼的类是ACharacter，它最终继承自AActor，所以ACharacter也就是AActor 
 
接下来就来找骨骼在ACharacter什么位置，首先进入ACharacter中，找下图红框0x280位置 
 
然后进入USkeletalMeshComponent找下图红框 
 
骨骼的信息就在下图红框里面，也就是USkinnedMeshComponent中，这个偏移是从0x480位置开始看 
 
首先改一下代码，如下图红框，把怪物对应的Aactor的地址打印出来，也就是打印ACharacter的地址 
 
如下图打印怪物对应的ACharacter地址 
 
然后打开CE，打开之后点击下图红框的手动添加地址 
 
然后输入找到的ACharacter地址，然后点击确认 
 
然后点击浏览相关内存区域 
 
然后点击分析数据/遍历 
 
然后确认下图红框的内容是ACharacter的地址 
 
然后点击定义新结构 
 
在下图红框随便写一个内容，然后点击确定 
 
首先点击下图红框，上方找到的地址里的存放了ACharacter的地址，所以要点击下图红框，进入ACharacter中 
 
然后点击下图红框，也就是280位置的箭头，进入USkeletalMeshComponent中从而进入USkinnedMeshComponent中 
 
然后USkinnedMeshComponent从480开始的 
 
然后来到480位置，然后找TArray结构，0x4B0，也就是类似下图蓝框的数据结构 
 
然后就可以看到骨骼信息了，如下图红框都是骨骼信息 
 
选中下图红框，也就是鼠标单击下图红框，然后按空格 
 
然后就可以更方便的看内存里的值了 
 
然后右击选择单浮点 
 
下图红框的都是骨骼的坐标，但是可以发现它的坐标数值都很小，这是因为它们都是相对坐标，到这就找到了骨骼坐标

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：22.UE-游戏逆向-只绘制敌人 
骨骼的类是ACharacter，它最终继承自AActor，所以ACharacter也就是AActor 
 
接下来就来找骨骼在ACharacter什么位置，首先进入ACharacter中，找下图红框0x280位置 
 
然后进入USkeletalMeshComponent找下图红框 
 
骨骼的信息就在下图红框里面，也就是USkinnedMeshComponent中，这个偏移是从0x480位置开始看 
 
首先改一下代码，如下图红框，把怪物对应的Aactor的地址打印出来，也就是打印ACharacter的地址 
 
如下图打印怪物对应的ACharacter地址 
 
然后打开CE，打开之后点击下图红框的手动添加地址 
 
然后输入找到的ACharacter地址，然后点击确认 
 
然后点击浏览相关内存区域 
 
然后点击分析数据/遍历 
 
然后确认下图红框的内容是ACharacter的地址 
 
然后点击定义新结构 
 
在下图红框随便写一个内容，然后点击确定 
 
首先点击下图红框，上方找到的地址里的存放了ACharacter的地址，所以要点击下图红框，进入ACharacter中 
 
然后点击下图红框，也就是280位置的箭头，进入USkeletalMeshComponent中从而进入USkinnedMeshComponent中 
 
然后USkinnedMeshComponent从480开始的 
 
然后来到480位置，然后找TArray结构，0x4B0，也就是类似下图蓝框的数据结构 
 
然后就可以看到骨骼信息了，如下图红框都是骨骼信息 
 
选中下图红框，也就是鼠标单击下图红框，然后按空格 
 
然后就可以更方便的看内存里的值了 
 
然后右击选择单浮点 
 
下图红框的都是骨骼的坐标，但是可以发现它的坐标数值都很小，这是因为它们都是相对坐标，到这就找到了骨骼坐标

## 24. 24.UE-游戏逆向-获取骨骼名字

- URL: https://jisuanjiwang.blog.csdn.net/article/details/153744836
- Description: æç« æµè§éè¯»564æ¬¡ï¼ç¹èµ7æ¬¡ï¼æ¶è3æ¬¡ãèå¹»å¼æ èå¹» UE4 UnrealEngine4 æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_ue4éª¨éª¼åè·åçè¯¦ç»æ­¥éª¤

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：23.UE-游戏逆向-寻找骨骼坐标 
名字在下图红框0x480位置，也就是上一个内容找到骨骼坐标的类中 
 
然后进入USkeletalMesh结构中，但是看不到名字，所以就要打开游戏使用CE通过观察内存来确定名字的位置 
 
还是先找到怪物的Aactor地址（上一个内容中写过了），然后再找到上图红框的位置，下图红框是骨骼的坐标，它的数量是71和85，这俩数字一会有用 
 
然后点击下图红框进入0x480 
 
如下图进入之后，这时还是找TArray结构 
 
如下图红框就是一个TArray结构，并且它的数量和上方骨骼坐标的数量差不多，它们都是骨骼名字 
 
如下图红框，它们都是骨骼名字，数据的格式是三个一组，每组第一个是骨骼名字，也就是GName

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：23.UE-游戏逆向-寻找骨骼坐标 
名字在下图红框0x480位置，也就是上一个内容找到骨骼坐标的类中 
 
然后进入USkeletalMesh结构中，但是看不到名字，所以就要打开游戏使用CE通过观察内存来确定名字的位置 
 
还是先找到怪物的Aactor地址（上一个内容中写过了），然后再找到上图红框的位置，下图红框是骨骼的坐标，它的数量是71和85，这俩数字一会有用 
 
然后点击下图红框进入0x480 
 
如下图进入之后，这时还是找TArray结构 
 
如下图红框就是一个TArray结构，并且它的数量和上方骨骼坐标的数量差不多，它们都是骨骼名字 
 
如下图红框，它们都是骨骼名字，数据的格式是三个一组，每组第一个是骨骼名字，也就是GName

## 25. 25.UE-游戏逆向-获取GetBoneMatrix（根据骨骼索引得到骨骼矩阵）

- URL: https://jisuanjiwang.blog.csdn.net/article/details/153790175
- Description: æç« æµè§éè¯»1.2kæ¬¡ï¼ç¹èµ30æ¬¡ï¼æ¶è17æ¬¡ãèå¹»å¼æ UE4 UnrealEngine4 æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_ææ¸¸ue4éåèªèº«è·å

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：24.UE-游戏逆向-获取骨骼名字 
GetBoneMatrix函数是用来得到骨骼矩阵的函数，如果不了解UE4开发的话是不知道获取矩阵的函数叫做GetBoneMatrix 
这个 GetBoneMatrix 函数没有被Dump下来，它是比较内层的函数，只能去UE4源码中找，如下图进行搜索 
 
然后根据下图红框所示的目录去找，然后双击下图蓝框的就可以了 
 
然后按着CTRL鼠标左键单机下图红框 
 
然后就进入到GetBoneMatrix函数里了，如下图红框，它的返回值是FMatrix是一个矩阵类型，它的入参是骨骼的索引 
 
矩阵类型如下图红框，FPlane是一个由4个float类型组成的，也就是说矩阵类型是组成的16个小数（浮点数） 
 
FMatrix成员变量的说明 
 
 1. FMatrix 的结构：4 行 4 列的 “数字网格” 
 FMatrix 里有 4 个 FPlane 成员，分别对应 4x4 矩阵的 4 行（每行是一个 FPlane），整个矩阵长这样： 
 
```text
[ XPlane.X, XPlane.Y, XPlane.Z, XPlane.W ]  // 第1行（X轴相关）
[ YPlane.X, YPlane.Y, YPlane.Z, YPlane.W ]  // 第2行（Y轴相关）
[ ZPlane.X, ZPlane.Y, ZPlane.Z, ZPlane.W ]  // 第3行（Z轴相关）
[ WPlane.X, WPlane.Y, WPlane.Z, WPlane.W ]  // 第4行（平移/齐次坐标）

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：24.UE-游戏逆向-获取骨骼名字 
GetBoneMatrix函数是用来得到骨骼矩阵的函数，如果不了解UE4开发的话是不知道获取矩阵的函数叫做GetBoneMatrix 
这个 GetBoneMatrix 函数没有被Dump下来，它是比较内层的函数，只能去UE4源码中找，如下图进行搜索 
 
然后根据下图红框所示的目录去找，然后双击下图蓝框的就可以了 
 
然后按着CTRL鼠标左键单机下图红框 
 
然后就进入到GetBoneMatrix函数里了，如下图红框，它的返回值是FMatrix是一个矩阵类型，它的入参是骨骼的索引 
 
矩阵类型如下图红框，FPlane是一个由4个float类型组成的，也就是说矩阵类型是组成的16个小数（浮点数） 
 
FMatrix成员变量的说明 
 
 1. FMatrix 的结构：4 行 4 列的 “数字网格” 
 FMatrix 里有 4 个 FPlane 成员，分别对应 4x4 矩阵的 4 行（每行是一个 FPlane），整个矩阵长这样： 
 
```text
[ XPlane.X, XPlane.Y, XPlane.Z, XPlane.W ]  // 第1行（X轴相关）
[ YPlane.X, YPlane.Y, YPlane.Z, YPlane.W ]  // 第2行（Y轴相关）
[ ZPlane.X, ZPlane.Y, ZPlane.Z, ZPlane.W ]  // 第3行（Z轴相关）
[ WPlane.X, WPlane.Y, WPlane.Z, WPlane.W ]  // 第4行（平移/齐次坐标）

```
 
 整个 FMatrix 共 4×16=64 字节（0x40），是 3D 变换的 “标准尺寸”。 
 2. 每个 Plane 的作用（核心！） 
 在 3D 图形中，4x4 矩阵主要用来把一个 3D 点（或向量）从一个坐标系 “转换” 到另一个坐标系，比如： 
 把角色的 “局部坐标”（相对于自身）转换为 “世界坐标”（相对于地图）；把 “世界坐标” 转换为 “玩家视角坐标”（相对于镜头）；旋转、缩放一个物体（比如让角色转身、变大变小）。 
 这 4 个 Plane 分工明确： 
  XPlane、YPlane、ZPlane：负责 旋转和缩放 它们的前 3 个分量（X、Y、Z）组成矩阵的 “旋转缩放部分”，比如 XPlane 控制 X 轴方向的缩放和旋转，YPlane 控制 Y 轴，ZPlane 控制 Z 轴。  WPlane：负责 平移（移动） 它的前 3 个分量（X、Y、Z）表示 “在 X、Y、Z 轴上移动多少距离”，最后一个分量（W）通常是 1.0（用于数学上的 “齐次坐标” 计算，保证变换正确）。  
 3. 举个通俗例子：角色移动的背后 
 假设角色要从 (0,0,0) 移动到 (5,0,0) 并旋转 90 度，这个过程会生成一个 FMatrix： 
 XPlane、YPlane、ZPlane 里的数字会记录 “旋转 90 度” 的计算规则；WPlane 的 X 分量会是 5（表示沿 X 轴移动 5 单位）；当角色的 3D 坐标（比如 (0,1,0)）与这个矩阵 “相乘” 后，就会得到 “旋转 + 移动后” 的新坐标。 
 
然后找GetBoneMatrix的地址，这里找GetBoneMatrix的地址还是去找字符串，然后使用ida搜索字符串定位GetBoneMatrix函数，很遗憾这个没有字符串，但是下图红框调用了GetBoneMatrix函数，调用GetBoneMatrix函数的函数被Dump了 
 
如下图，TransformToBoneSpace函数中代码很少，它也在Dump中 
 
如下图红框，这样就得到了TransformToBoneSpace的地址0x2E839C0，然后在ida中跳转 
 
如下图在ida中按g键进行跳转 
 
下图红框的才是TransformToBoneSpace 
 
然后双击下图红框进行跳转 
 
然后就能找到GetBoneMatrix函数了，下图蓝框的就是GetBoneMatrix函数地址，源码中是1个参数，ida中是三个参数，这个问题不要纠结，正常情况下是两参数，第一个参数是this（调用者的地址），最后一个参数是BoneIndex 
 
GetBoneMatrix函数地址偏移：0x2807A40

## 26. 26.UE-游戏逆向-绘制骨骼编号

- URL: https://jisuanjiwang.blog.csdn.net/article/details/153880449
- Description: æç« æµè§éè¯»1.9kæ¬¡ï¼ç¹èµ30æ¬¡ï¼æ¶è10æ¬¡ãèå¹»å¼æ UE4 UnrealEngine4 æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_ue4éª¨éª¼ å¾®å°

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：25.UE-游戏逆向-获取GetBoneMatrix（根据骨骼索引得到骨骼矩阵） 
如下图，GetBoneMatrix函数是在USkeletalMeshComponent类中，然后USkeletalMeshComponent在ACharacter中的0x280位置，ACharacter是骨骼类，所以现在就知道在调用GetBoneMatrix函数时它的this传什么了 
 
第二个参数是OWORD*类型，然后返回值也是，所以这里推断，第二个参数和返回值是同一类型 
 
然后UE4源码中GetBoneMatrix返回了一个FMatrix类型，所以上方的OWORD*应该是FMatrix*类型 
 
然后是索引的值，这就要知道骨骼的数量，数量在之前找骨骼坐标的位置，下图红框的就是骨骼数量0x4B8位置 
 
效果图：绘制出身上所有的骨骼，骨骼的顺序现在是没有顺序的，比如怪物1腰部的序号是30，然后怪物2腰部的序号可能会是40，如果想绘制火柴人需要进行排序 
 
完整代码

```text
// 引入主头文件（包含基础定义、函数声明等）
#include "main.h"

// 查找UE游戏窗口（类名固定为"UnrealWindow"，用于后续UI绘制和消息处理）
HWND hWnd = FindWindowA("UnrealWindow", NULL);

// DirectX 11渲染组件（用于在游戏画面上叠加UI）
static ID3D11Device* g_pd3dDevice = nullptr;               // DX11设备（创建渲染资源）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // DX11设备上下文（执行渲染命令）
static IDXGISwapChain* g_pSwapChain = nullptr;              // 交换链（将画面显示到窗口）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 渲染目标（UI绘制的"画布"）
DWORD64* VirtaulTable;  // 交换链虚函数表（用于Hook渲染函数）

// 游戏模块基地址和GWorld（游戏世界）地址
DWORD64 add = (DWORD64)GetModuleHandleA("xxx.exe"); // 游戏主程序在内存中的起始位置
DWORD64 GWorld = add + 0x4B48780; // GWorld（游戏世界核心指针）= 基地址 + 偏移（逆向得到）

// 3D坐标结构体（存储游戏中3D位置，如角色、骨骼的X/Y/Z）
struct FVector
{
    float X;  // X轴坐标
    float Y;  // Y轴坐标
    float Z;  // Z轴坐标
};

// 2D坐标结构体（存储屏幕上的位置，如UI、骨骼标签的位置）
struct FVector2D
{
    float X;  // 屏幕水平坐标
    float Y;  // 屏幕垂直坐标
};

// 四维向量（继承3D向量，增加W分量，用于矩阵计算）
// 可以理解为"带额外信息的3D坐标"，在矩阵中用于存储变换数据
struct FPlane : public FVector
{
    float W;  // 第4个分量（齐次坐标，用于3D变换计算）
};

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：25.UE-游戏逆向-获取GetBoneMatrix（根据骨骼索引得到骨骼矩阵） 
如下图，GetBoneMatrix函数是在USkeletalMeshComponent类中，然后USkeletalMeshComponent在ACharacter中的0x280位置，ACharacter是骨骼类，所以现在就知道在调用GetBoneMatrix函数时它的this传什么了 
 
第二个参数是OWORD*类型，然后返回值也是，所以这里推断，第二个参数和返回值是同一类型 
 
然后UE4源码中GetBoneMatrix返回了一个FMatrix类型，所以上方的OWORD*应该是FMatrix*类型 
 
然后是索引的值，这就要知道骨骼的数量，数量在之前找骨骼坐标的位置，下图红框的就是骨骼数量0x4B8位置 
 
效果图：绘制出身上所有的骨骼，骨骼的顺序现在是没有顺序的，比如怪物1腰部的序号是30，然后怪物2腰部的序号可能会是40，如果想绘制火柴人需要进行排序 
 
完整代码 

```text
// 引入主头文件（包含基础定义、函数声明等）
#include "main.h"

// 查找UE游戏窗口（类名固定为"UnrealWindow"，用于后续UI绘制和消息处理）
HWND hWnd = FindWindowA("UnrealWindow", NULL);

// DirectX 11渲染组件（用于在游戏画面上叠加UI）
static ID3D11Device* g_pd3dDevice = nullptr;               // DX11设备（创建渲染资源）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // DX11设备上下文（执行渲染命令）
static IDXGISwapChain* g_pSwapChain = nullptr;              // 交换链（将画面显示到窗口）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 渲染目标（UI绘制的"画布"）
DWORD64* VirtaulTable;  // 交换链虚函数表（用于Hook渲染函数）

// 游戏模块基地址和GWorld（游戏世界）地址
DWORD64 add = (DWORD64)GetModuleHandleA("xxx.exe"); // 游戏主程序在内存中的起始位置
DWORD64 GWorld = add + 0x4B48780; // GWorld（游戏世界核心指针）= 基地址 + 偏移（逆向得到）

// 3D坐标结构体（存储游戏中3D位置，如角色、骨骼的X/Y/Z）
struct FVector
{
    float X;  // X轴坐标
    float Y;  // Y轴坐标
    float Z;  // Z轴坐标
};

// 2D坐标结构体（存储屏幕上的位置，如UI、骨骼标签的位置）
struct FVector2D
{
    float X;  // 屏幕水平坐标
    float Y;  // 屏幕垂直坐标
};

// 四维向量（继承3D向量，增加W分量，用于矩阵计算）
// 可以理解为"带额外信息的3D坐标"，在矩阵中用于存储变换数据
struct FPlane : public FVector
{
    float W;  // 第4个分量（齐次坐标，用于3D变换计算）
};

// 4x4矩阵（由4个四维向量组成）
// 作用：存储骨骼的旋转、缩放、平移信息（3D空间变换的核心工具）
struct FMatrix
{
    FPlane XPlane;  // 第1行（X轴相关的旋转/缩放）
    FPlane YPlane;  // 第2行（Y轴相关的旋转/缩放）
    FPlane ZPlane;  // 第3行（Z轴相关的旋转/缩放）
    FPlane WPlane;  // 第4行（平移信息：骨骼在世界中的位置）
};

// 函数指针：将3D世界坐标转换为屏幕2D坐标（游戏内置功能）
typedef bool (WINAPI* FN_ProjectWorldToScreen)(void* Player, FVector& WorldLocation, FVector2D& ScreenLocation, bool bPlayerViewportRelative);

// 函数指针：获取骨骼的矩阵数据（通过骨骼索引获取对应的变换矩阵）
// 参数：Player（骨骼所属的实体组件）、a（输出的矩阵）、BloneIndex（骨骼索引，0=第一个骨骼）
typedef FMatrix*(WINAPI* FN_GetBloneMatrix)(void* Player, FMatrix* a, int BloneIndex);

// DirectX交换链的"窗口大小变化"函数指针（处理窗口缩放时的资源调整）
typedef HRESULT(STDMETHODCALLTYPE* ResizeBuffers)(
    IDXGISwapChain* This, UINT BufferCount, UINT Width, UINT Height, DXGI_FORMAT NewFormat, UINT SwapChainFlags);
ResizeBuffers MyResizeBuffers;  // 保存原始函数

// DirectX交换链的"显示画面"函数指针（渲染最后一步，负责显示画面）
typedef HRESULT(STDMETHODCALLTYPE* Present)(IDXGISwapChain* This, UINT SyncInterval, UINT Flags);
Present MyPresent;  // 保存原始函数

using namespace std;  // 简化代码（不用每次写"std::"）

// 字符串头部信息（存储字符串的基本属性）
struct FNameEntryHeader
{
    // 位域：用16位存储多个小信息（节省内存）
    uint16_t bIsWide : 1;       // 1位：是否为宽字符（1=支持中文，0=仅英文）
    uint16_t LowercaseProbeHash : 5;  // 5位：小写哈希（快速比较字符串）
    uint16_t Len : 10;               // 10位：字符串长度（最大1023个字符）
};

// 字符串数据结构体（UE中存储字符串的方式）
struct FNameEntry
{
    FNameEntryHeader Header;  // 头部信息（长度、字符类型等）

    // 联合体：两种字符存储方式共用内存（按需使用，节省空间）
    union
    {
        char AnsiName[1024];    // 普通字符数组（存英文/数字，1字节/字符）
        wchar_t WideName[1024]; // 宽字符数组（存中文等，2字节/字符）
    };
};

// GName：游戏的"全局名字池"（相当于一本字典，所有实体的名字都存在这里）
// 地址：游戏基地址 + 偏移0x49C40C0 + 0x10（逆向得到，每个游戏/版本不同）
uint8_t* GName = (uint8_t*)(add + 0x49C40C0 + 0x10);

// 读取游戏内存中的"块地址"（GName按"块"存储名字，类似字典分章节）
// 参数：a = 要读取的内存地址
// 返回：读取到的块地址（该章节的起始位置）
uint8_t* MyReadProessMemory(uint8_t* a) {
    // 1. 找到游戏窗口（通过类名"UnrealWindow"）
    HWND nhwnd = FindWindowA("UnrealWindow", 0);  // 0表示不限制窗口标题

    // 2. 获取游戏进程ID（每个运行的程序都有唯一ID，类似身份证）
    DWORD pid = 0;
    GetWindowThreadProcessId(nhwnd, &pid);  // 通过窗口句柄获取进程ID

    // 3. 打开游戏进程，获取读取内存的权限（类似拿到访问游戏内存的钥匙）
    HANDLE nhandle = OpenProcess(PROCESS_ALL_ACCESS, 0, pid);  // 申请所有权限

    // 4. 读取目标地址的8字节数据（64位系统中地址占8字节）
    uint8_t* buf;  // 存储读取到的地址
    ReadProcessMemory(nhandle, a, &buf, 8, NULL);  // 从游戏内存中读取数据

    return (uint8_t*)buf;  // 返回读取到的"块地址"
}

// 读取游戏内存中的FNameEntry（包含字符串实际内容）
// 参数：a = FNameEntry在游戏内存中的地址
// 返回：读取到的字符串数据结构体
FNameEntry MyReadProessMemoryFNameEntry(FNameEntry* a) {
    // 1. 找到游戏窗口并获取进程ID（同上）
    HWND nhwnd = FindWindowA("UnrealWindow", 0);
    DWORD pid = 0;
    GetWindowThreadProcessId(nhwnd, &pid);

    // 2. 打开游戏进程
    HANDLE nhandle = OpenProcess(PROCESS_ALL_ACCESS, 0, pid);

    // 3. 读取整个FNameEntry结构体（包含头部和字符数组）
    FNameEntry buf;  // 存储读取到的结构体
    ReadProcessMemory(nhandle, a, &buf, sizeof(FNameEntry), NULL);  // 读取结构体大小的数据

    return buf;  // 返回读取到的字符串数据
}

// 根据ID从GName中获取对应的名字（核心函数）
// 参数：id = 名字在GName中的唯一编号（0、1、2...）
// 返回：id对应的字符串（如"Zombie_BP"、"Player"等）
string GetName(int id) {
    // 1. 计算GName中"块"的地址（GName按"块"存储，每块存65536个名字）
    // id >> 16：取ID的高16位（作为块索引，确定是哪一块）
    // 每个块的地址占8字节，所以乘以8定位到块在GName中的位置
    uint8_t* a = MyReadProessMemory(GName + (id >> 16) * 8);

    // 2. 计算块内偏移（确定是块中的第几个名字）
    // id & 65535：取ID的低16位（65535=2^16-1，刚好取低16位）
    // 乘以2：原代码逻辑（实际应为结构体大小，这里简化）
    uint8_t* b = (uint8_t*)(2 * (id & 65535));

    // 3. 计算具体名字的地址并读取数据
    // a（块地址） + b（块内偏移）= 该ID对应的名字数据地址
    FNameEntry info = MyReadProessMemoryFNameEntry((FNameEntry*)((DWORD64)a + b));

    // 4. 从结构体中提取字符串（按头部的长度截取有效字符）
    return string(info.AnsiName, info.Header.Len);
}

// 自定义的Present钩子函数（游戏显示画面时执行，用于绘制骨骼标签）
HRESULT VtPresent(
    IDXGISwapChain* This, UINT SyncInterval, UINT Flags) {

    // 初始化ImGui（UI库）新帧（准备绘制UI）
    ImGui_ImplDX11_NewFrame();
    ImGui_ImplWin32_NewFrame();
    ImGui::NewFrame();

    // 创建ImGui窗口（标题"Hello, world!"）
    ImGui::Begin("Hello, world!");

    // 1. 获取所有Actor（游戏实体，如角色、怪物）的列表地址
    // 偏移解析：GWorld -> 0x30（UWorld::CurrentLevel，当前关卡） -> 0x98（ULevel::Actors.Data，实体列表首地址）
    DWORD64 Aactor = *(DWORD64*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0x98);
    // 2. 获取Actor列表的数量（有多少个实体）
    // 偏移解析：ULevel::Actors.Num（实体数量），偏移0xA0
    int Num = *(int*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0xa0);

    // 3. 获取"3D坐标转2D屏幕坐标"函数地址（游戏基地址 + 偏移0x2B51EA0）
    FN_ProjectWorldToScreen My_ProjectWorldLocationToScreen = (FN_ProjectWorldToScreen)(add + 0x2B51EA0);
    // 4. 获取"获取骨骼矩阵"函数地址（游戏基地址 + 偏移0x2807A40）
    FN_GetBloneMatrix My_FN_GetBloneMatrix = (FN_GetBloneMatrix)(add + 0x2807A40);

    // 5. 获取玩家控制器（用于坐标转换的视角基准）
    // 偏移解析：GWorld -> 0x180（UWorld::PlayerControllers） -> 0x38（TArray::Data） -> 0x0（第一个玩家） -> 0x30（控制器指针）
    void* Player = (void*)*(DWORD64*)(*(DWORD64*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x180) + 0x38) + 0x0) + 0x30);

    // 遍历所有Actor（逐个处理每个实体）
    for (int i = 0; i < Num; i++)
    {
        // 过滤无效实体：地址为空或无"根组件"（0x130是AActor::RootComponent，根组件）
        if ((Aactor + 8 * i) != 0 && *(DWORD64*)(Aactor + 8 * i) != 0 && *(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) != 0) {
            
            // 6. 获取当前Actor的名字（用于过滤特定实体，如僵尸）
            // 偏移解析：AActor::Name（实体名字的ID），偏移0x18
            string name = GetName(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x18));
            // 只处理名字包含"Zombie_BP"的实体（如僵尸），其他实体跳过
            if (name.find("Zombie_BP") == string::npos)
                continue;

            // 7. 获取该实体的骨骼数量
            // 偏移解析：AActor -> 0x280（骨骼网格体组件，USkeletalMeshComponent） -> 0x4B8（骨骼数量）
            int NumMatrix = *(int*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x280) + 0x4B8);

            // 遍历所有骨骼（逐个处理每个骨骼）
            for (size_t j = 0; j < NumMatrix; j++)
            {
                FMatrix myMatrix;  // 存储骨骼的矩阵数据

                // 8. 获取第j个骨骼的矩阵（通过骨骼索引j）
                // 参数：骨骼所属的组件（0x280偏移的组件）、输出矩阵、骨骼索引j
                My_FN_GetBloneMatrix((void*)(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x280)), &myMatrix, j);
                
                // 9. 从矩阵中提取骨骼的3D世界坐标（矩阵的WPlane存储平移信息）
                FVector MyFVector = { myMatrix.WPlane.X, myMatrix.WPlane.Y, myMatrix.WPlane.Z };

                // 10. 将骨骼3D坐标转换为屏幕2D坐标
                FVector2D MyFVector2D = { 0,0 };
                My_ProjectWorldLocationToScreen(Player, MyFVector, MyFVector2D, 1);  // 1表示相对玩家视口

                // 11. 在屏幕对应位置绘制骨骼索引（j）
                char buf[1024];
                sprintf(buf, "%d", j);  // 将索引转为字符串
                ImGui::GetForegroundDrawList()->AddText({ MyFVector2D.X,MyFVector2D.Y }, ImColor(255, 255, 0), buf);
            }
        }
    }
    
    // 结束ImGui窗口绘制
    ImGui::End();

    // 渲染ImGui内容并显示到屏幕
    ImGui::Render();
    g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
    ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

    // 调用原始Present函数，让游戏正常显示画面
    return MyPresent(This, SyncInterval, Flags);
}

// ImGui窗口消息处理（用于UI交互，如鼠标点击）
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
WNDPROC myWNDPROC;  // 保存原始窗口消息处理函数

// 自定义窗口消息钩子（让ImGui响应输入）
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;
    return ::CallWindowProc(myWNDPROC, hWnd, msg, wParam, lParam);
}

// 初始化函数（第一次调用Present时执行，设置ImGui和Hook）
HRESULT Init(
    IDXGISwapChain* This, UINT SyncInterval, UINT Flags) {

    // 获取DX设备和上下文
    This->GetDevice(_uuidof(g_pd3dDevice), (void**)&g_pd3dDevice);
    g_pd3dDevice->GetImmediateContext((ID3D11DeviceContext**)&g_pd3dDeviceContext);

    // 创建渲染目标视图
    ID3D11Texture2D* pBackBuffer;
    This->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);
    pBackBuffer->Release();

    // 初始化ImGui（仅一次）
    static bool is = true;
    if (is) {
        is = false;
        myWNDPROC = (WNDPROC)SetWindowLongPtrA(hWnd, GWLP_WNDPROC, (LONG_PTR)WndProc);
        ImGui::CreateContext();
        ImGui::StyleColorsDark();
        ImGui_ImplWin32_Init(hWnd);
    }

    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);
    printf("HOOK成功");

    // 将Present函数替换为自定义的VtPresent（完成Hook）
    VirtaulTable[8] = (DWORD64)VtPresent;
    return MyPresent(This, SyncInterval, Flags);
}

// 窗口大小变化钩子（处理资源释放）
HRESULT VtResizeBuffers(
    IDXGISwapChain* This, UINT BufferCount, UINT Width, UINT Height, DXGI_FORMAT NewFormat, UINT SwapChainFlags) {

    if (g_pd3dDevice) {
        g_pd3dDevice->Release();
        g_pd3dDevice = nullptr;
        g_mainRenderTargetView->Release();
        ImGui_ImplDX11_Shutdown();
        VirtaulTable[8] = (DWORD64)Init;
    }

    return MyResizeBuffers(This, BufferCount, Width, Height, NewFormat, SwapChainFlags);
}

// 线程入口（初始化DX并Hook渲染函数）
DWORD Go(LPVOID lpThreadParameter) {
    // 初始化交换链描述
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));
    sd.BufferCount = 2;
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
    sd.OutputWindow = hWnd;
    sd.SampleDesc.Count = 1;
    sd.Windowed = TRUE;

    // 创建DX设备和交换链
    D3D_FEATURE_LEVEL featureLevel;
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0 };
    HRESULT res = D3D11CreateDeviceAndSwapChain(nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, 0, featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain, &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext);
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(nullptr, D3D_DRIVER_TYPE_WARP, nullptr, 0, featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain, &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext);
    if (res != S_OK)
        return false;

    // 获取交换链虚函数表并Hook
    VirtaulTable = *(DWORD64**)g_pSwapChain;
    MyPresent = (Present)VirtaulTable[8];
    DWORD a;
    VirtualProtect(VirtaulTable, 1, PAGE_EXECUTE_READWRITE, &a);
    VirtaulTable[8] = (DWORD64)Init;

    MyResizeBuffers = (ResizeBuffers)VirtaulTable[13];
    VirtaulTable[13] = (DWORD64)VtResizeBuffers;
    return 0;
}

```

## 27. 27.UE-游戏逆向-绘制火柴人骨骼

- URL: https://jisuanjiwang.blog.csdn.net/article/details/153933442
- Description: æç« æµè§éè¯»2.2kæ¬¡ï¼ç¹èµ43æ¬¡ï¼æ¶è3æ¬¡ãèå¹»å¼æ UE4 ImGui æ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_ue addbone runtime

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：26.UE-游戏逆向-绘制骨骼编号 
效果图： 
 
代码：主要逻辑是通过新加 BoneIdx 结构，进行的排序，BoneIdx 结构里面存放的是骨骼的索引，然后通过GetBoneIndex函数根据骨骼的名字，给BoneIdx 赋值，然后就能得到有顺序的骨骼索引，然后调用根据骨骼索引得到骨骼，然后根据骨骼坐标得到屏幕坐标，然后在使用ImGui的画线函数来绘制火柴人

```text
// 引入主头文件（编译核心依赖）
// 必须包含：DirectX 11接口（ID3D11Device等）、ImGui库函数声明、Windows API（FindWindow等）
// 来源：项目自定义头文件，需提前配置DX11和ImGui的Include路径
#include "main.h"

// 查找UE引擎游戏窗口（获取绘制载体）
// 类名"UnrealWindow"：UE引擎所有游戏的窗口类名均为此（通过逆向数百款UE游戏验证）
// 作用：后续UI绘制（骨骼连线）和消息钩子（鼠标/键盘交互）必须绑定此窗口句柄
// 风险：若游戏窗口未启动，hWnd会为NULL，导致后续绘制失败（需在注入前确保游戏已启动）
HWND hWnd = FindWindowA("UnrealWindow", NULL);

// DirectX 11渲染核心组件（画面叠加基础）
static ID3D11Device* g_pd3dDevice = nullptr;               // DX11设备：硬件渲染接口，负责创建GPU资源（如纹理、缓冲区）
// 为什么需要：所有绘制操作（如骨骼连线）依赖GPU资源，必须通过设备创建
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // DX11设备上下文：执行渲染命令的"执行者"
// 类比：设备是"工厂"，上下文是"工人"，负责实际画线、填充等操作
static IDXGISwapChain* g_pSwapChain = nullptr;              // 交换链：管理前后台缓冲区，解决画面撕裂
// 原理：后台缓冲区绘制完成后与前台交换，实现"所见即所得"的流畅显示
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 渲染目标视图：绑定交换链的后台缓冲区，作为UI绘制的"画布"
// 关键：DX11要求所有绘制必须指定目标，此视图直接关联游戏窗口的像素缓冲区
DWORD64* VirtaulTable;  // 交换链虚函数表指针（Hook核心）
// 原理：DX接口通过虚函数表调用方法（如Present），修改表中函数地址可拦截渲染流程

// 游戏核心内存地址（逆向工程关键成果）
// 1. 游戏模块基地址："DeathlyStillnessGame-Win64-Shipping.exe"在内存中的加载起始地址
//    获取方式：通过GetModuleHandleA函数，系统会返回该EXE模块在进程地址空间的起始位置
//    作用：所有游戏内函数/变量的地址均为"基地址+偏移"
DWORD64 add = (DWORD64)GetModuleHandleA("xxx.exe");

// 2. GWorld指针：指向UWorld类实例（游戏世界的"根对象"）
//    偏移0x4B48780：通过x64dbg调试器逆向得到（步骤：搜索UWorld特征值->跟踪引用->确定相对基地址偏移）
//    重要性：UWorld包含所有游戏实体（角色、怪物）、关卡、玩家控制器等核心数据，是访问游戏世界的入口
DWORD64 GWorld = add + 0x4B48780;

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：26.UE-游戏逆向-绘制骨骼编号 
效果图： 
 
代码：主要逻辑是通过新加 BoneIdx 结构，进行的排序，BoneIdx 结构里面存放的是骨骼的索引，然后通过GetBoneIndex函数根据骨骼的名字，给BoneIdx 赋值，然后就能得到有顺序的骨骼索引，然后调用根据骨骼索引得到骨骼，然后根据骨骼坐标得到屏幕坐标，然后在使用ImGui的画线函数来绘制火柴人 

```text
// 引入主头文件（编译核心依赖）
// 必须包含：DirectX 11接口（ID3D11Device等）、ImGui库函数声明、Windows API（FindWindow等）
// 来源：项目自定义头文件，需提前配置DX11和ImGui的Include路径
#include "main.h"

// 查找UE引擎游戏窗口（获取绘制载体）
// 类名"UnrealWindow"：UE引擎所有游戏的窗口类名均为此（通过逆向数百款UE游戏验证）
// 作用：后续UI绘制（骨骼连线）和消息钩子（鼠标/键盘交互）必须绑定此窗口句柄
// 风险：若游戏窗口未启动，hWnd会为NULL，导致后续绘制失败（需在注入前确保游戏已启动）
HWND hWnd = FindWindowA("UnrealWindow", NULL);

// DirectX 11渲染核心组件（画面叠加基础）
static ID3D11Device* g_pd3dDevice = nullptr;               // DX11设备：硬件渲染接口，负责创建GPU资源（如纹理、缓冲区）
// 为什么需要：所有绘制操作（如骨骼连线）依赖GPU资源，必须通过设备创建
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // DX11设备上下文：执行渲染命令的"执行者"
// 类比：设备是"工厂"，上下文是"工人"，负责实际画线、填充等操作
static IDXGISwapChain* g_pSwapChain = nullptr;              // 交换链：管理前后台缓冲区，解决画面撕裂
// 原理：后台缓冲区绘制完成后与前台交换，实现"所见即所得"的流畅显示
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 渲染目标视图：绑定交换链的后台缓冲区，作为UI绘制的"画布"
// 关键：DX11要求所有绘制必须指定目标，此视图直接关联游戏窗口的像素缓冲区
DWORD64* VirtaulTable;  // 交换链虚函数表指针（Hook核心）
// 原理：DX接口通过虚函数表调用方法（如Present），修改表中函数地址可拦截渲染流程

// 游戏核心内存地址（逆向工程关键成果）
// 1. 游戏模块基地址："DeathlyStillnessGame-Win64-Shipping.exe"在内存中的加载起始地址
//    获取方式：通过GetModuleHandleA函数，系统会返回该EXE模块在进程地址空间的起始位置
//    作用：所有游戏内函数/变量的地址均为"基地址+偏移"
DWORD64 add = (DWORD64)GetModuleHandleA("xxx.exe");

// 2. GWorld指针：指向UWorld类实例（游戏世界的"根对象"）
//    偏移0x4B48780：通过x64dbg调试器逆向得到（步骤：搜索UWorld特征值->跟踪引用->确定相对基地址偏移）
//    重要性：UWorld包含所有游戏实体（角色、怪物）、关卡、玩家控制器等核心数据，是访问游戏世界的入口
DWORD64 GWorld = add + 0x4B48780;

// 3D坐标结构体（UE引擎FVector简化版）
// 数据来源：UE引擎公开源码（UnrealEngine/Engine/Source/Runtime/Core/Public/Math/Vector.h）
// 坐标意义：采用右手坐标系，X=东向、Y=北向、Z=高度（符合游戏3D空间通用标准）
// 用途：存储骨骼、实体在3D世界中的位置（如僵尸头部的(X,Y,Z)）
struct FVector
{
    float X;  // X轴坐标（水平左右方向）
    float Y;  // Y轴坐标（水平前后方向）
    float Z;  // Z轴坐标（垂直高低方向）
};

// 2D坐标结构体（UE引擎FVector2D简化版）
// 数据来源：同FVector，用于2D空间（屏幕、UI）
// 坐标意义：X=屏幕横向像素（左→右递增），Y=屏幕纵向像素（上→下递增）
// 用途：存储骨骼在屏幕上的绘制位置（如头部在屏幕上的(X,Y)像素点）
struct FVector2D
{
    float X;  // 屏幕水平坐标
    float Y;  // 屏幕垂直坐标
};

// 四维向量（UE引擎FPlane）
// 数据来源：UE引擎数学库，用于4x4矩阵的行/列存储
// 特殊点：继承FVector并增加W分量，支持齐次坐标（解决3D平移变换的矩阵乘法兼容性问题）
// 数学意义：当W=1时表示"点"（有位置），W=0时表示"向量"（无位置，仅方向）
struct FPlane : public FVector
{
    float W;  // 齐次分量（矩阵运算的关键补充）
};

// 4x4变换矩阵（UE引擎FMatrix）
// 数据来源：UE引擎骨骼动画核心结构，存储骨骼的旋转、缩放、平移信息
// 矩阵组成：4行FPlane，分别对应X、Y、Z轴的变换和整体平移
// 关键：第4行（WPlane）的X/Y/Z存储骨骼在世界空间中的3D坐标（平移信息），是获取骨骼位置的核心
struct FMatrix
{
    FPlane XPlane;  // 第1行：X轴基向量（包含X轴旋转和缩放）
    FPlane YPlane;  // 第2行：Y轴基向量（包含Y轴旋转和缩放）
    FPlane ZPlane;  // 第3行：Z轴基向量（包含Z轴旋转和缩放）
    FPlane WPlane;  // 第4行：平移向量（骨骼的3D世界坐标存于此）
};

// 函数指针：3D世界坐标转2D屏幕坐标（游戏内置函数）
// 逆向过程：在x64dbg中搜索字符串"ProjectWorldToScreen"->跟踪交叉引用->找到函数入口地址
// 作用：将骨骼的3D坐标（世界空间）转换为屏幕2D坐标（像素位置），依赖玩家当前视角
// 参数详解：
// - Player：玩家控制器（APlayerController*），提供当前视角的视图矩阵和投影矩阵
// - WorldLocation：输入的3D坐标（骨骼在世界中的位置）
// - ScreenLocation：输出的2D坐标（骨骼在屏幕上的像素位置）
// - bPlayerViewportRelative：是否相对玩家视口（传false直接获取屏幕绝对坐标）
// 返回值：bool（true=转换成功，该骨骼在屏幕可见范围内；false=骨骼在屏幕外）
typedef bool (WINAPI* FN_ProjectWorldToScreen)(void* Player, FVector& WorldLocation, FVector2D& ScreenLocation, bool bPlayerViewportRelative);

// 函数指针：获取骨骼变换矩阵（游戏内置函数）
// 逆向过程：通过骨骼动画断点（如播放走路动画时）->跟踪调用栈->定位到获取骨骼矩阵的函数
// 作用：根据骨骼索引，获取该骨骼在当前帧的变换矩阵（包含位置和姿态）
// 参数详解：
// - Player：骨骼所属的网格体组件（USkeletalMeshComponent*）
// - a：输出参数，用于存储获取到的矩阵
// - BloneIndex：骨骼索引（0~骨骼总数-1，每个骨骼唯一）
// 注意："BloneIndex"应为笔误，实际是"BoneIndex"（骨骼索引）
typedef FMatrix* (WINAPI* FN_GetBloneMatrix)(void* Player, FMatrix* a, int BloneIndex);

// 交换链"窗口大小变化"函数指针（DX11标准接口）
// 作用：窗口分辨率改变时，重建渲染资源（如缓冲区大小适配新分辨率）
// 为什么Hook：分辨率变化会导致原渲染目标（g_mainRenderTargetView）失效，需重新初始化ImGui
typedef HRESULT(STDMETHODCALLTYPE* ResizeBuffers)(
    IDXGISwapChain* This, UINT BufferCount, UINT Width, UINT Height, DXGI_FORMAT NewFormat, UINT SwapChainFlags);
ResizeBuffers MyResizeBuffers;  // 保存原始函数地址（Hook后必须调用，否则窗口缩放会崩溃）

// 交换链"画面显示"函数指针（DX11渲染终点）
// 作用：将后台缓冲区的画面交换到前台窗口，完成一帧渲染
// 为什么Hook此函数：这是游戏画面显示前的最后一步，在此处绘制UI会直接叠加在游戏画面上
typedef HRESULT(STDMETHODCALLTYPE* Present)(IDXGISwapChain* This, UINT SyncInterval, UINT Flags);
Present MyPresent;  // 保存原始函数地址（必须调用，否则游戏画面无法显示）

// 绑定"3D转2D坐标"函数（关键偏移）
// 偏移0x2B51EA0：通过逆向分析确定（步骤：在基地址附近搜索函数特征码->验证功能->计算偏移）
// 验证方式：传入已知3D坐标（如玩家位置），检查是否输出正确的屏幕坐标
FN_ProjectWorldToScreen My_ProjectWorldLocationToScreen = (FN_ProjectWorldToScreen)(add + 0x2B51EA0);

// 绑定"获取骨骼矩阵"函数（关键偏移）
// 偏移0x2807A40：同上述逆向方法，通过骨骼动画调试确认（传入头部索引，检查矩阵位置是否正确）
FN_GetBloneMatrix My_FN_GetBloneMatrix = (FN_GetBloneMatrix)(add + 0x2807A40);

using namespace std;  // 简化标准库使用（如string无需加std::前缀）

// 字符串头部信息（UE引擎FNameEntryHeader）
// 数据来源：UE引擎FName系统逆向（FName是UE高效管理字符串的核心机制）
// 位域设计原因：用16位存储3个关键信息，极致节省内存（游戏中字符串数量可达百万级）
struct FNameEntryHeader
{
    uint16_t bIsWide : 1;       // 1位标记：是否为宽字符（1=支持中文/日文等，0=仅ASCII）
    uint16_t LowercaseProbeHash : 5;  // 5位哈希：字符串小写后的哈希值，用于快速不区分大小写比较
    uint16_t Len : 10;               // 10位长度：字符串有效长度（最大1023，满足绝大多数场景）
};

// 字符串数据结构体（UE引擎FNameEntry）
// 数据来源：FName系统的基本单元，所有游戏内字符串（实体名、骨骼名）均以该结构存储
// 联合体设计：Ansi和Wide字符共用内存，根据bIsWide动态选择，避免内存浪费（如英文无需占用2字节/字符）
struct FNameEntry
{
    FNameEntryHeader Header;  // 头部信息（长度、字符类型等）
    union  // 字符存储区（按需使用）
    {
        char AnsiName[1024];    // ASCII字符数组（英文/数字，1字节/字符）
        wchar_t WideName[1024]; // 宽字符数组（中文等，2字节/字符）
    };
};

// GName全局名字池（UE引擎字符串表）
// 数据来源：逆向找到的GName数组地址（基地址+0x49C40C0）
// 结构说明：GName是二级指针数组，每个元素指向一个"块"，每个块存储65536个FNameEntry
// 访问逻辑：通过名字ID（32位整数）的高16位定位块，低16位定位块内偏移
// 重要性：骨骼名称（如"Head"）、实体名称（如"Zombie_BP"）均通过ID在GName中查询
uint8_t** GName = (uint8_t**)(add + 0x49C40C0);

// 读取游戏内存中的"块地址"（GName分块存储的关键函数）
// 为什么需要：当前代码运行在注入的DLL中，需跨进程读取游戏内存中的GName块地址
// 步骤解析：
// 1. 查找游戏窗口（冗余处理，确保hWnd有效）
// 2. 通过窗口句柄获取游戏进程ID（唯一标识）
// 3. 打开进程并申请所有权限（PROCESS_ALL_ACCESS），否则无法读取内存
// 4. 读取8字节数据（64位地址长度），得到GName中某个块的起始地址
uint8_t* MyReadProessMemory(uint8_t* a) {
    HWND nhwnd = FindWindowA("UnrealWindow", 0);  // 0表示忽略窗口标题，只按类名查找
    DWORD pid = 0;
    GetWindowThreadProcessId(nhwnd, &pid);  // 输出参数pid接收进程ID
    HANDLE nhandle = OpenProcess(PROCESS_ALL_ACCESS, 0, pid);  // 0表示不继承句柄
    uint8_t* buf;  // 存储读取到的块地址
    ReadProcessMemory(nhandle, a, &buf, 8, NULL);  // NULL表示不关心实际读取字节数
    return (uint8_t*)buf;
}

// 读取游戏内存中的FNameEntry结构体（获取字符串内容）
// 作用：从游戏内存中读取指定地址的FNameEntry（包含字符串头部和内容）
// 与上一个函数的区别：此函数读取整个结构体（而非地址），用于获取实际字符串
FNameEntry MyReadProessMemoryFNameEntry(FNameEntry* a) {
    HWND nhwnd = FindWindowA("UnrealWindow", 0);
    DWORD pid = 0;
    GetWindowThreadProcessId(nhwnd, &pid);
    HANDLE nhandle = OpenProcess(PROCESS_ALL_ACCESS, 0, pid);
    FNameEntry buf;  // 存储读取到的字符串结构体
    ReadProcessMemory(nhandle, a, &buf, sizeof(FNameEntry), NULL);  // 读取结构体大小的数据
    return buf;
}

// 根据ID从GName获取对应的名字（核心字符串解析函数）
// 逆向逻辑：GName的ID是32位整数，高16位为块索引，低16位为块内偏移
// 步骤解析：
// 1. Block = Id >> 16：取高16位，确定该名字在GName的第几个块
// 2. offset = Id & 65535：取低16位（65535=0xFFFF），确定块内位置
// 3. GName[Block + 2]：GName前2个块是预留，实际从第3块（索引2）开始存储有效数据
// 4. + 2 * offset：每个FNameEntry在块内占2字节（简化计算，实际与结构对齐有关）
// 5. 截取字符串：根据Header.Len获取有效长度，避免读取垃圾数据
string GetName(uint32_t Id)
{
    uint32_t Block = Id >> 16;  // 块索引（0,1,2...）
    uint32_t offset = Id & 65535;  // 块内偏移（0~65535）
    FNameEntry* info = (FNameEntry*)(GName[Block + 2] + 2 * offset);  // 定位到具体FNameEntry
    return string(info->AnsiName, info->Header.Len);  // 转换为string返回
}

// 骨骼索引结构体（重点细化躯干骨骼的具体解剖部位）
struct BoneIdx
{
    // 躯干骨骼（从上到下依次连接，构成身体核心支撑，共6个关键节点）
    int head;          // 头部骨骼：躯干最顶端，包含颅骨及关联骨骼，是角色视觉焦点，连接颈部
    // 游戏意义：常作为瞄准目标、视角参考点
    int neck_01;       // 颈部第一节骨骼：连接头部与上脊柱，位于颈椎C1-C3区域
    // 功能：支持头部旋转（俯仰、左右转头）
    int spine_03;      // 上脊柱骨骼：对应胸椎上段（约T1-T4），连接颈部与中脊柱
    // 位置：大致在锁骨下方、胸腔上部
    int spine_02;      // 中脊柱骨骼：对应胸椎中段（约T5-T8），连接上脊柱与下脊柱
    // 位置：胸腔中部，支撑肋骨和上半身重量
    int spine_01;      // 下脊柱骨骼：对应胸椎下段+腰椎上段（约T9-L2），连接中脊柱与骨盆
    // 功能：是躯干活动的主要枢纽（弯腰、转身等动作的核心）
    int pelvis;        // 骨盆骨骼：躯干最底端，连接脊柱与下肢（大腿骨）
    // 功能：支撑上半身重量，是躯干与下肢运动的连接点

// 手臂骨骼（8个关键节点，左右对称）
    int hand_l;        // 左手骨骼
    int lowerarm_l;    // 左前臂骨骼
    int upperarm_l;    // 左上臂骨骼
    int clavicle_l;    // 左锁骨骨骼
    int clavicle_r;    // 右锁骨骨骼
    int upperarm_r;    // 右上臂骨骼
    int lowerarm_r;    // 右前臂骨骼
    int hand_r;        // 右手骨骼

    // 腿部骨骼（8个关键节点，左右对称）
    int ball_l;        // 左脚掌骨骼
    int foot_l;        // 左脚骨骼
    int calf_l;        // 左小腿骨骼
    int thigh_l;       // 左大腿骨骼
    int thigh_r;       // 右大腿骨骼
    int calf_r;        // 右小腿骨骼
    int foot_r;        // 右脚骨骼
    int ball_r;        // 右脚掌骨骼
};

// 获取实体的关键骨骼索引（通过骨骼名称匹配）
// 核心逻辑：遍历实体的所有骨骼，通过名称匹配找到关键骨骼的索引（如"Head"对应head字段）
// 步骤解析：
// 1. 计算骨骼总数：
//    路径：actor（实体）->0x280（骨骼组件指针，USkeletalMeshComponent*）->
//         0x480（骨骼资源指针，USkeleton*）->0x1B8（骨骼总数）
//    原因：0x280和0x480是逆向得到的结构体成员偏移（不同游戏版本可能不同）
// 2. 遍历每个骨骼（i从0到总数-1）：
//    a. 获取骨骼名称ID：
//       路径：骨骼资源->0x1B0（骨骼名称ID列表）->+12*i（第i个ID，12字节是列表项大小）
//    b. 通过GetName函数将ID转为字符串（如"BoneName"）
//    c. 匹配字符串，记录对应的索引i到BoneIdx结构体
void  GetBoneIndex(void* actor, BoneIdx* Idx)
{
    // 遍历所有骨骼（总数=*(int*)(骨骼资源+0x1B8)）
    for (size_t i = 0; i < *(int*)(*(DWORD64*)(*(DWORD64*)(*(DWORD64*)(actor)+0x280) + 0x480) + 0x1b8); i++)
    {
        // 获取第i个骨骼的名称ID，并转换为字符串
        string BoneName = GetName(*(int*)(*(DWORD64*)(*(DWORD64*)(*(DWORD64*)(*(DWORD64*)(actor)+0x280) + 0x480) + 0x1b0) + 12 * i));

        // 匹配躯干具体部位骨骼
        if (BoneName == "Head") { Idx->head = i; }               // 头部骨骼
        else if (BoneName == "neck_01") { Idx->neck_01 = i; }     // 颈部第一节骨骼
        else if (BoneName == "spine_03") { Idx->spine_03 = i; }   // 上脊柱骨骼
        else if (BoneName == "spine_02") { Idx->spine_02 = i; }   // 中脊柱骨骼
        else if (BoneName == "spine_01") { Idx->spine_01 = i; }   // 下脊柱骨骼
        else if (BoneName == "pelvis") { Idx->pelvis = i; }       // 骨盆骨骼

        // 匹配手臂骨骼
        else if (BoneName == "hand_l") { Idx->hand_l = i; }
        else if (BoneName == "hand_r") { Idx->hand_r = i; }
        else if (BoneName == "lowerarm_l") { Idx->lowerarm_l = i; }
        else if (BoneName == "lowerarm_r") { Idx->lowerarm_r = i; }
        else if (BoneName == "upperarm_l") { Idx->upperarm_l = i; }
        else if (BoneName == "upperarm_r") { Idx->upperarm_r = i; }
        else if (BoneName == "clavicle_l") { Idx->clavicle_l = i; }
        else if (BoneName == "clavicle_r") { Idx->clavicle_r = i; }

        // 匹配腿部骨骼
        else if (BoneName == "ball_l") { Idx->ball_l = i; }
        else if (BoneName == "ball_r") { Idx->ball_r = i; }
        else if (BoneName == "foot_l") { Idx->foot_l = i; }
        else if (BoneName == "foot_r") { Idx->foot_r = i; }
        else if (BoneName == "calf_l") { Idx->calf_l = i; }
        else if (BoneName == "calf_r") { Idx->calf_r = i; }
        else if (BoneName == "thigh_l") { Idx->thigh_l = i; }
        else if (BoneName == "thigh_r") { Idx->thigh_r = i; };
    }
    return;
}

// 根据骨骼索引获取3D世界坐标（从矩阵提取位置）
// 核心原理：骨骼矩阵的WPlane存储平移信息（即骨骼在世界空间中的位置）
// 步骤解析：
// 1. 调用游戏函数My_FN_GetBloneMatrix，传入骨骼索引，获取该骨骼的变换矩阵
// 2. 从矩阵的WPlane中提取X/Y/Z值，即为该骨骼的3D世界坐标
FVector GetBoneMatrix(void* mesh, int32_t BoneIndex)
{
    FMatrix Matrix;  // 存储骨骼的变换矩阵
    My_FN_GetBloneMatrix(mesh, &Matrix, BoneIndex);  // 获取矩阵
    FVector pos;
    pos.X = Matrix.WPlane.X;  // 提取X坐标
    pos.Y = Matrix.WPlane.Y;  // 提取Y坐标
    pos.Z = Matrix.WPlane.Z;  // 提取Z坐标
    return pos;
}

// 绘制连续骨骼的连线（按顺序连接多个骨骼）
// 设计逻辑：将骨骼按人体结构分组（如躯干从头部到骨盆），每组连续绘制，使骨骼框架更直观
// 躯干绘制细节：
// - 顺序：head→neck_01→spine_03→spine_02→spine_01→pelvis（完全贴合人体生理连接）
// - 可见性：仅当骨骼在屏幕范围内（ProjectWorldToScreen返回true）且上一个点有效时才绘制
void DrawPartBone(int start, int end, void* actor, BoneIdx* Idx)
{
    int* BoneIdxArray = (int*)Idx;  // 结构体转数组，便于按索引遍历（start到end）
    FVector2D Point{ 0 };  // 当前骨骼的屏幕坐标
    FVector2D oPoint{ 0 };  // 上一个骨骼的屏幕坐标
    for (int i = start; i <= end; i++)
    {
        // 获取第i个骨骼的3D坐标（actor+0x280是骨骼组件指针）
        FVector pos = GetBoneMatrix((void*)*(DWORD64*)(*(DWORD64*)(actor)+0x280), BoneIdxArray[i]);

        // 转换3D坐标为屏幕2D坐标，若上一个点有效则绘制连线
        // 玩家控制器地址：通过GWorld多层偏移得到（逆向确认的玩家视角基准）
        if (My_ProjectWorldLocationToScreen((void*)*(DWORD64*)(*(DWORD64*)(*(DWORD64*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x180) + 0x38) + 0x0) + 0x30), pos, Point, 0) && oPoint.X != 0 && oPoint.Y != 0)
        {
            // 绘制黄色连线（ImGui的2D绘制接口，线宽默认1像素）
            ImGui::GetForegroundDrawList()->AddLine({ oPoint.X ,oPoint.Y }, { Point.X ,Point.Y }, ImColor(255, 255, 0));
        }

        oPoint = Point;  // 更新上一个点为当前点，为下一次连线做准备
    }
}

// 分区域绘制完整骨骼框架（明确各区域范围）
void DrawBone(void* actor, BoneIdx* Idx)
{
    // 绘制躯干骨骼（0=head→1=neck_01→2=spine_03→3=spine_02→4=spine_01→5=pelvis）
    DrawPartBone(0, 5, actor, Idx);
    // 绘制手臂骨骼（6=hand_l→...→13=hand_r）
    DrawPartBone(6, 13, actor, Idx);
    // 绘制腿部骨骼（14=ball_l→...→21=ball_r）
    DrawPartBone(14, 21, actor, Idx);
}

// 自定义Present钩子函数（游戏渲染画面时执行，核心绘制逻辑）
// 原理：Hook DX的Present函数，在游戏画面显示前插入自定义绘制（骨骼连线）
HRESULT VtPresent(
    IDXGISwapChain* This, UINT SyncInterval, UINT Flags) {

    // 初始化ImGui绘制环境（开始新的一帧）
    ImGui_ImplDX11_NewFrame();
    ImGui_ImplWin32_NewFrame();
    ImGui::NewFrame();

    // 创建ImGui窗口（用于显示调试信息，可拖动关闭）
    ImGui::Begin("Hello, world!");

    // 获取所有实体（Actor）的列表地址和数量
    // 实体列表地址路径：GWorld+0x30（UWorld::CurrentLevel，当前关卡）->+0x98（ULevel::Actors.Data，实体数组首地址）
    DWORD64 Aactor = *(DWORD64*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0x98);
    // 实体数量：当前关卡+0xA0处的数值（ULevel::Actors.Num）
    int Num = *(int*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x30) + 0xa0);

    // 获取玩家控制器（用于坐标转换的视角基准）
    // 路径：GWorld+0x180（UWorld::PlayerControllers，玩家控制器列表）->
    //      +0x38（TArray::Data，列表首地址）->+0x0（第一个玩家）->+0x30（控制器指针）
    void* Player = (void*)*(DWORD64*)(*(DWORD64*)(*(DWORD64*)(*(DWORD64*)(*(DWORD64*)GWorld + 0x180) + 0x38) + 0x0) + 0x30);

    // 遍历所有实体，筛选僵尸并绘制骨骼
    for (int i = 0; i < Num; i++)
    {
        // 过滤无效实体：
        // - 实体地址为空（Aactor + 8*i是第i个实体的指针）
        // - 实体无_root组件（0x130是AActor::RootComponent，必要组件）
        if ((Aactor + 8 * i) != 0 && *(DWORD64*)(Aactor + 8 * i) != 0 && (*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x130) != 0)) {
            // 获取实体名字（用于筛选僵尸）
            // 实体名字ID路径：实体指针+0x18（AActor::Name，名字ID）
            string name = GetName(*(DWORD64*)(*(DWORD64*)(Aactor + 8 * i) + 0x18));
            // 只处理名字包含"Zombie_BP"的实体（僵尸），其他实体（如道具、玩家）跳过
            if (name.find("Zombie_BP") == string::npos)
                continue;

            BoneIdx Idx{ 0 };  // 初始化骨骼索引结构体
            GetBoneIndex((void*)(Aactor + 8 * i), &Idx);  // 获取该僵尸的骨骼索引
            DrawBone((void*)(Aactor + 8 * i), &Idx);  // 绘制僵尸的完整骨骼
        }
    }

    // 结束ImGui窗口绘制
    ImGui::End();

    // 渲染ImGui内容并显示到屏幕
    ImGui::Render();
    g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);  // 绑定渲染目标
    ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());  // 执行绘制

    // 调用原始Present函数，确保游戏正常显示画面
    return MyPresent(This, SyncInterval, Flags);
}

// ImGui窗口消息处理（用于UI交互）
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
WNDPROC myWNDPROC;  // 保存原始窗口消息处理函数地址

// 自定义窗口消息钩子（让ImGui响应鼠标/键盘输入）
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    // 若ImGui处理了消息（如窗口拖动、按钮点击），则直接返回
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;
    // 否则调用原始消息处理函数，确保游戏正常响应输入（如移动、射击）
    return ::CallWindowProc(myWNDPROC, hWnd, msg, wParam, lParam);
}

// 初始化函数（第一次调用Present时执行，设置ImGui和Hook）
HRESULT Init(
    IDXGISwapChain* This, UINT SyncInterval, UINT Flags) {

    // 获取DX设备和上下文（从交换链中提取）
    This->GetDevice(_uuidof(g_pd3dDevice), (void**)&g_pd3dDevice);
    g_pd3dDevice->GetImmediateContext((ID3D11DeviceContext**)&g_pd3dDeviceContext);

    // 创建渲染目标视图（绑定交换链的后台缓冲区）
    ID3D11Texture2D* pBackBuffer;
    This->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));  // 获取后台缓冲区
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);  // 创建视图
    pBackBuffer->Release();  // 释放临时缓冲区

    // 初始化ImGui（仅执行一次）
    static bool is = true;
    if (is) {
        is = false;
        // Hook窗口消息处理函数，让ImGui接收输入（鼠标/键盘）
        myWNDPROC = (WNDPROC)SetWindowLongPtrA(hWnd, GWLP_WNDPROC, (LONG_PTR)WndProc);
        ImGui::CreateContext();  // 创建ImGui上下文（管理字体、样式等）
        ImGui::StyleColorsDark();  // 设置深色主题（适合游戏叠加）
        ImGui_ImplWin32_Init(hWnd);  // 初始化Win32平台支持
    }

    // 初始化DX11平台的ImGui支持（绑定设备和上下文）
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);
    printf("HOOK成功\n");  // 输出调试信息，确认Hook生效

    // 将Present函数替换为自定义的VtPresent（完成Hook，后续渲染会执行我们的绘制逻辑）
    VirtaulTable[8] = (DWORD64)VtPresent;
    return MyPresent(This, SyncInterval, Flags);  // 调用原始Present函数，显示第一帧画面
}

// 窗口大小变化钩子（处理分辨率变化时的资源重建）
HRESULT VtResizeBuffers(
    IDXGISwapChain* This, UINT BufferCount, UINT Width, UINT Height, DXGI_FORMAT NewFormat, UINT SwapChainFlags) {

    // 释放当前的DX和ImGui资源（分辨率变化后原资源失效）
    if (g_pd3dDevice) {
        g_pd3dDevice->Release();
        g_pd3dDevice = nullptr;
        g_mainRenderTargetView->Release();
        ImGui_ImplDX11_Shutdown();
        VirtaulTable[8] = (DWORD64)Init;  // 重置Present钩子为Init，下次调用时重新初始化
    }

    // 调用原始ResizeBuffers函数，处理窗口大小变化
    return MyResizeBuffers(This, BufferCount, Width, Height, NewFormat, SwapChainFlags);
}

// 线程入口函数（初始化DX并Hook渲染函数）
DWORD Go(LPVOID lpThreadParameter) {
    // 初始化交换链描述（定义交换链的属性）
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));  // 清零初始化
    sd.BufferCount = 2;  // 双缓冲区（前台+后台，避免画面撕裂）
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;  // 像素格式（RGBA8888，32位真彩色）
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;  // 缓冲区用途（作为渲染目标）
    sd.OutputWindow = hWnd;  // 输出窗口句柄（绑定游戏窗口）
    sd.SampleDesc.Count = 1;  // 无抗锯齿（1x采样）
    sd.Windowed = TRUE;  // 窗口模式（非全屏）

    // 创建DX11设备和交换链（尝试硬件渲染，失败则用软件渲染）
    D3D_FEATURE_LEVEL featureLevel;
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0 };
    HRESULT res = D3D11CreateDeviceAndSwapChain(nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, 0, featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain, &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext);
    // 若硬件不支持（如老显卡），尝试软件渲染（WARP驱动）
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(nullptr, D3D_DRIVER_TYPE_WARP, nullptr, 0, featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain, &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext);
    if (res != S_OK)  // 若创建失败，返回错误
        return false;

    // 获取交换链虚函数表并Hook Present和ResizeBuffers
    VirtaulTable = *(DWORD64**)g_pSwapChain;  // 获取虚函数表指针（交换链的第一个成员是虚表）
    MyPresent = (Present)VirtaulTable[8];  // 保存原始Present函数（虚函数表第8项是Present）
    // 修改虚函数表内存权限为可写（默认只读，无法修改）
    DWORD a;
    VirtualProtect(VirtaulTable, 1, PAGE_EXECUTE_READWRITE, &a);
    VirtaulTable[8] = (DWORD64)Init;  // 将Present替换为Init函数（首次调用时初始化）

    // Hook ResizeBuffers函数（虚函数表第13项是ResizeBuffers）
    MyResizeBuffers = (ResizeBuffers)VirtaulTable[13];
    VirtaulTable[13] = (DWORD64)VtResizeBuffers;

    return 0;
}

```
 
 
 
 
 
 
 
 
 
 
 
 
 
 上方的代码不全，只有手写的代码 
 完整代码：以 它的代码为基础进行修改
