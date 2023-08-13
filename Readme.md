
この成果物は教育用のものであり、実際の医療診断には使用しないでください。

## 動機
放射線科医不在の外勤先で、健診などで胸部x線の画像の読影をする機会が多い。見落とし防止のためAIを利用したい。無料で！!

## 使用方法
"Load image"ボタンで読影して欲しい画像を読み込み。Aに読み込み画像を表示。疾患名とその疾患である確率をBに表示。Bの疾患名をクリックするとCにその疾患に割り当てられた根拠がヒートマップとしてCに表示(下図のCはBの"Mass"をクリックした結果)。

![スクリーンショット 2023-08-13 131957.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/612743/b9504c53-9198-0213-dfa8-9de8ce39d2db.png)

## 使用モデル
arXivに公開されているモデルを使用[^1]。torchxrayvisionとしてパッケージ化されており、再配布可能なライセンスで公開されている。
具体的な成績については下記とのこと。縦軸がデータセットで横軸がモデル名。今回は一番右の列の"All"のモデルを使用している。食道ヘルニアや胸水の診断については優秀そうだが、結節影や骨折の診断は苦手そう。
![auc-all.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/612743/c68d1510-4c5b-cc53-92ec-a00cbf70246e.jpeg)


## 感想
紛らわしい症例については結局50%程度の確率になってしまい、得られる情報は少ない。結局健診で悩ましいような画像は再検査に回してCTを撮ってもらうしかないか。残念。。。
例で示してるようなMassなんて誰が見ても明らかやねんから、90%以上の確率で診断してくれよ。ただ見落としの防止については一定の効果があるかも？
モデルをもっと有効なものに入れ替えるなり改善すれば、もうちょっと優秀になるかな。


[^1]: Cohen, J. P. et al. TorchXRayVision: A library of chest X-ray datasets and models. Preprint at http://arxiv.org/abs/2111.00595 (2021).
