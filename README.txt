FDTD & Model generators


Img2Kcell
	svgz線画-->png画像-->FDTD解析モデルの形状データ、を順に作成

	Inkscapeでsvgz形状を作成（スキャナ画像から）
	線画内部を黒に塗りつぶす
	pixel数を指定してpng画像をexport
	pythonプログラムでFDTD法用のデータに変換
	(1) img2kcell1.py [余盛りあり]
	(2) img2kcell2.py [余盛りなし]
	２つのプログラムは同じ。入力データに応じてトリミング範囲が
	変わるため、統合せずに別プログラムとして保管している

FDM(FDTD法関連のプログラムとデータ)
 |--Bead (data folder, 余盛り有り)
 |--Bead0(data folder 余盛りなし)
 |--Input(input data sample)
 |--Src(C++ source code)

FDM/ 直下のbinary code:
	fdm2d: FDTD法プログラムの実行形式
	plot_inwv: 入力波形データのみ計算して出力(使用する必要なし)
FDM/ 直下のpython program
	bscan.py, ascans.py  :　走時波形の表示
	dbscan.py: 走時波形の差画像（散乱波成分を表示）
	vsnap.py: 速度場のスナップショットを表示
	dvsnap.py: 散乱波動場(２つの速度場の差分)のスナップショット
	kcell.py: モデル形状の表示
		(fdm2dを実行したときに作成されるkcell.datを読み込んで表示)

Data Folder(Bead, Bead0)以下の構成
	Bead
	 |--Far
	 |--Near
	 |--P70deg
