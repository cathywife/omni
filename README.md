## omni ##
运维管理平台

硬件生命周期
    采购阶段：
><li>采购申请</li>
><li>采购审核
><li>选择供应商 </li>
        开始采购
        采购成功
    使用阶段：
        资产录入
        上线服役
        故障维修
        老龄退役
    回收处理：
        配件利用
        彻底废弃

服务器、交换机、路由器、防火墙、F5等设备状态:
    关机
    开机
    待机
    维护
    宕机
    不可达
    

CPU 
内存
硬盘： SATA SAS SSD   2.5 3.5
光驱
网卡： 电口  光口 1000M  10000M
电源
阵列卡


生产厂商  产品类型  品牌  系列  型号
经销商


主机   主机组

salt-call state.sls app.web_proxy.nginx
state  --> state组 --> 项目标签
全局state
主机/组 --> 项目标签
主机/组 --> state/组



1 通过ewf发起资源申请
2 管理泳道/业务的集群,进行资源池资源分配
3 通过eoc应用配置,部署服务
4 管理tengine, 能够区分业务集群,分别管理配置文件,包括lua限流策略
5 维护集群物理架构,能够配置服务集群间的上下依赖关系,比如:web-proxy至web.mux/web.httpizza/web.api的依赖关系



服务器逻辑信息表
主机与群组关系表
应用信息表

除以上3各表外,所有数据在自由mysql数据库内存储.


服务部署流程: 资源申请 CMDB主机组划分 goproxy服务注册 泳道信息配置文件关系 配置应用 代码部署 huskar配置变更 服务重启 域名解析 接入F5 验收

tengine限流仅实现基于location的QPS限制, 打点



泳道
主机组
产品
appid

泳道逻辑架构,即泳道模型,存在版本的概念,每个泳道实例也都有各自版本,以便进行灰度
业务 + 泳道    逻辑架构


服务器
主机组
AppID
配置(eoc job, ewf, saltstate, cmd; 版本升级时,需保持整洁)    泳道、集群、APPID各自存在特定配置

反向代理(goproxy, haproxy, tengine等配置管理/升级)
fastcgi(hhvm, php-fpm)
服务管理(supervisor, service, systemd)
agent部署(elk, esm, eoc, zabbix)
zabbix模板添加
crontab
泳道配置(env.yaml)
解释器(python,java)
日志轮转
appid配置(eless, husker, 代码内默认配置)
goproxy(注册appid, 应用配置对应连接串: 127.0.0.1:port)
服务下线(停服务,清理,提下线申请)
健康检查
各服务间关联精确至端口级别(通过端口连线)


主机组 -> 集群 -> 集群模板

服务依赖关系管理:
    调用方式: SOA直连   nginx七层代理    goproxy代理
    app_id间的依赖调用关系
    通过app_id间的依赖关系和app_id部署集群, 自动生成该集群goproxy注册信息

