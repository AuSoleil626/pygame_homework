# pygame_homework
外卖员大战外星人

classDiagram
    class Singleton {
        - instance : Singleton
        - Singleton()
        + getInstance() : Singleton
        + someBusinessLogic() : void
    }

    note right of Singleton
        - instance: 静态私有变量，用于存储单例实例
        - Singleton(): 私有构造函数，防止外部实例化
        + getInstance(): 公共静态方法，用于获取单例实例
        + someBusinessLogic(): 其他业务方法
    end note
