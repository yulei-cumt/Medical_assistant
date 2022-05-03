# 调用意图分类模型
import torch
import numpy as np
from importlib import import_module
import argparse

parser = argparse.ArgumentParser(description='Chinese Text Classification')
parser.add_argument('--model', type=str, default='TextCNN', required=True, help='choose a model: TextCNN, TextRNN, FastText, TextRCNN, TextRNN_Att, DPCNN, Transformer')
parser.add_argument('--embedding', default='pre_trained', type=str, help='random or pre_trained')
parser.add_argument('--word', default=False, type=bool, help='True for word, False for char')
args = parser.parse_args()


class callModelCNN:
    def __init__(self):
        self.className = ['disease_department',
                     'disease_symptom',
                     'symptom_disease',
                     'disease_cause',
                     'disease_acompany',
                     'disease_not_food',
                     'disease_do_food',
                     'food_not_disease',
                     'food_do_disease',
                     'disease_drug',
                     'drug_disease',
                     'disease_check',
                     'check_disease',
                     'disease_prevent',
                     'disease_lasttime',
                     'disease_cureway',
                     'disease_cureprob',
                     'disease_easyget',
                     'disease_desc']

    def callCNN(self):
        # 搜狗:embedding_SougouNews.npz, 腾讯:embedding_Tencent.npz, 随机初始化:random
        embedding = 'embedding_SougouNews.npz'
        if args.embedding == 'random':
            embedding = 'random'
        model_name = args.model  # TextCNN, TextRNN,
        if model_name == 'FastText':
            from intentions.utils_fasttext import build_dataset, build_iterator, get_time_dif
            embedding = 'random'
        else:
            from intentions.utils import build_dataset, build_iterator, get_time_dif

        dataset = 'intentions/THUCNews'  # 数据集
        x = import_module('intentions.models.' + model_name)
        config = x.Config(dataset, embedding)
        model = x.Model(config).to(config.device)

        model.load_state_dict(torch.load(config.save_path))
        model.eval()
        vocab, train_data, dev_data, test_data = build_dataset(config, args.word)
        test_iter = build_iterator(test_data, config)
        # with torch.no_grad():
        for i, (test, labels) in enumerate(test_iter):
            outputs = model(test)
            # print('outputs************', i,  outputs)
        out = outputs.detach().numpy().tolist()
        out = out[0]
        return self.className[out.index(max(out))]


if __name__ == '__main__':
    handler = callModelCNN()
    ans = handler.callCNN()
    print(ans)