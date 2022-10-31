import os


def train():
    cmd = 'python -m spacy train config.cfg --gpu-id 0 --output ./ ' \
          '--paths.train ./training_data.spacy --paths.dev ./val_data.spacy'
    print("TRAINING STARTED")
    os.system(cmd)
    print("TRAINING FINISHED")


train()
