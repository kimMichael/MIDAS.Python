# ------------------------------------------------------------------------------
# Copyright 2020 Rui LIU (@liurui39660)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# 	http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

from pathlib import Path

from numpy import around
from pandas import read_csv
from sklearn.metrics import roc_auc_score
from tqdm import tqdm
import csv

from MIDAS import FilteringCore, NormalCore, RelationalCore

if __name__ == '__main__':
	root = (Path(__file__) / '../..').resolve()
	label = read_csv(root / "data/project/july.week5.800mb.csv.truth", header=None, squeeze=True, dtype=int)
	# midas = NormalCore(2, 1024)
	# midas = RelationalCore(2, 1024)
	midas = FilteringCore(2, 1024, 1e3)
	score = [0.] * label.shape[0]
	with open(root / "data/project/july.week5.800mb.csv.processed", 'r') as file:
		for i in tqdm(range(label.shape[0]), unit_scale=True):  # Much faster than pandas indexing
			data = file.readline().split(',')
			score[i] = midas(int(data[1]), int(data[2]), int(data[0])+1) #adding 1 to t index
	#score = around(score, 6)  # Same as c++ version
	#score.tofile(root / "temp/ScoreF.txt", '\n')
	with open(root / "temp/ScoreF3.txt", 'w', newline='') as out:
		dict_writer = csv.DictWriter(out, score[0].keys())
		dict_writer.writeheader()
		dict_writer.writerows(score)

	print(f"ROC-AUC = {roc_auc_score(label, [max(x.values()) for x in score]):.4f}")
	print(f"# Raw anomaly scores will be exported to")
	print(f"# {root / 'temp/ScoreF3.txt'}")
