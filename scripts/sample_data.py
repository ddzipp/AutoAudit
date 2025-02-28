import pandas as pd
from datasets import load_dataset

ds = load_dataset("trendmicro-ailab/Primus-Seed", split="train")

df = pd.DataFrame(ds)

df = df.iloc[1:]

sampled_df = df.sample(n=2000, random_state=42)

sampled_df.to_csv('sampled_primus_seed.csv', index=False)