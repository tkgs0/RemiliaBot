# RemiliaBot
女生自用(?)电报机器人

### 使用方法

1. 安装Python3并配置好环境变量
2. 创建一个空文件夹, 在命令行cd到该文件夹下
3. 输入以下命令安装并运行

```sh
pip install remilia-bot   # 从 PyPI 安装 Bot
python -m remilia   # 运行 Bot
```

### 功能表

- [x] **/start**  
  查看当前会话ID, 通常私聊的会话ID会与用户ID相同  
  
- [x] **/code** 在线跑代码

  <details>
    <summary>使用方法</summary>

  ```
  /code python
  print('不可以色色')
  ```

  </details>

- [x] **/de64** 六十四卦解密文本

  <details>
    <summary>使用方法</summary>

  ```
  /de64 ䷙䷴䷂䷷䷙䷭䷪䷌䷙䷴䷰䷔䷄䷎䷐䷻䷄䷎䷐䷻
  ```

  </details>

- [x] **/en64** 六十四卦加密文本

  <details>
    <summary>使用方法</summary>

  ```
  /en64 不可以色色
  ```

  </details>

- [x] **/pix** 来点色图

  <details>
    <summary>使用方法</summary>

  ```
  /pix   # 随机一张涩图
  /pix 3   # 随机三张涩图
  /pix 阿波尼亚   # 发一张 '阿波尼亚' 的涩图
  /pix 3 阿波尼亚   # 发三张 '阿波尼亚' 的涩图
  /pix 3 崩坏3 阿波尼亚   # 发三张 '崩坏3' '阿波尼亚' 的涩图
  ```

  </details>

- [x] **/setu** 来点色图  
  用法同 `/pix`  
  
- [x] **/status**  
  查询机器人状态  
  
- [x] **/awc** 会话响应 - 加白指定会话

  <details>
    <summary>使用方法</summary>

  ```
  /awc id id1 id2 ...
  ```

  </details>

- [x] **/dwc** 会话屏蔽 - 屏蔽指定会话

  <details>
    <summary>使用方法</summary>

  ```
  /dwc id id1 id2 ...
  ```

  </details>

- [x] **/awu** 用户响应 - 加白指定用户

  <details>
    <summary>使用方法</summary>

  ```
  /awu id id1 id2 ...
  ```

  </details>

- [x] **/dwu** 用户屏蔽 - 拉黑指定用户

  <details>
    <summary>使用方法</summary>

  ```
  /dwu id id1 id2 ...
  ```

  </details>

- [x] **/wake** 唤醒  
  响应当前会话  
  
- [x] **/sleep** 睡觉  
  屏蔽当前会话  

- [x] **闲聊功能**  
  在你要对Bot说的骚话前面加上Bot的昵称并发送  
  (昵称在config.yml中设置, 不是你在BotFather设置的Bot用户名)
