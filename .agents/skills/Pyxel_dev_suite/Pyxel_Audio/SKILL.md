name: Pyxel Audio
description: >
  Pyxel における効果音 (Sound) と音楽 (Music) の再生・管理、
  およびBGMの自動生成を自動化するスキル。
  .pyxres からの読み込みだけでなく、プロシージャルなサウンド作成もサポートする。

instructions: |
  - ユーザーが効果音や BGM の再生、停止、生成に関する要求をした場合に発火する。
  - 以下の処理を自動化する：
      - 指定チャンネルでのサウンド再生 (`pyxel.play(ch, snd, loop)`)
      - ミュージックの再生 (`pyxel.playm(msc, loop)`)
      - 全サウンドの停止 (`pyxel.stop()`)
      - BGMの自動生成 (`pyxel.gen_bgm(preset, instr, seed, play)`)
  - 4チャンネル同時発音と、64サウンド / 8ミュージックの仕様を前提とする。

inputs:
  - task: 再生 (play) / 停止 (stop) / 音楽再生 (playm) / BGM生成 (gen_bgm)
  - sound_id / music_id: リソースの番号
  - channel: 再生チャンネル (0-3)

outputs:
  - 再生制御用のメソッドまたは関数
  - プロシージャルオーディオ（自動生成BGM）の呼び出しコード
