name: Pyxel Audio
description: >
  Pyxel における効果音 (Sound) と音楽 (Music) の再生・管理、
  およびBGMの自動生成を自動化するスキル。
  .pyxres からの読み込みだけでなく、プロシージャルなサウンド作成もサポートする。

instructions: |
  - ユーザーが効果音や BGM の再生、停止、生成に関する要求をした場合に発火する。
  - 以下の Pyxel 2.7.8 準拠の処理を自動化する：
      - **サウンド定義**: `pyxel.sounds[n].set(notes, tones, volumes, effects, speed)` を使用する。
      - **ミュージック定義**: `pyxel.musics[n].set(ch0_snds, ch1_snds, ch2_snds, ch3_snds)` を使用する。
      - **チャンネル制御**: 4チャンネル (0-3) の同時発音。Ch 0-1 を SFX、Ch 2-3 を BGM に割り当てるのがプロ仕様。
      - **プロシージャル BGM**: `pyxel.gen_bgm(preset, seed)` による動的生成。
      - **再生制御**: `pyxel.play(ch, snd, loop)`, `pyxel.playm(msc, loop)`, `pyxel.stop()` の活用。
  - 注意：`pyxel.sound(n)` や `pyxel.music(n)` は非推奨 (Deprecated) のため、必ず `pyxel.sounds[n]` / `pyxel.musics[n]` を使用する。

inputs:
  - task: 定義 (set) / 再生 (play) / 停止 (stop) / 音楽再生 (playm) / BGM生成 (gen_bgm)
  - sound_id / music_id: リソースの番号 (0-63 / 0-7)
  - channel: 再生チャンネル (0-3)

outputs:
  - Pyxel 2.7.8 準拠のオーディオ初期化および制御コード
  - `gen_bgm` を活用したプロシージャルな BGM 構成
