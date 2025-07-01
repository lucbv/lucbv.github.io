import pandas as pd
import json
import os

path = os.getcwd()
dirs = os.listdir(path)

benchmark_dirs = []
for dir in dirs:
    if(os.path.isdir(os.path.join(path, dir))):
        benchmark_dirs.append(os.path.join(path, dir))

data_dict = {'name': [],'date': [],'sha': [],'time': [],'time unit': []}
print(data_dict)
for benchmark_dir in benchmark_dirs:
    benchmark_files = os.listdir(benchmark_dir)
    for bfile in benchmark_files:
        if os.path.isfile(os.path.join(benchmark_dir, bfile)):
            filepath = os.path.join(benchmark_dir, bfile)
            f = open(filepath, "r")
            data = json.load(f)
            f.close()
            for benchIdx in range(len(data["benchmarks"])):
                data_dict["name"].append(data["benchmarks"][benchIdx]["name"])
                data_dict["date"].append(data["context"]["date"].split("T")[0])
                data_dict["sha"].append(data["context"]["GIT_COMMIT_HASH"])
                data_dict["time"].append(data["benchmarks"][benchIdx]["real_time"])
                data_dict["time unit"].append(data["benchmarks"][benchIdx]["time_unit"])

df = pd.DataFrame.from_dict(data_dict)
df["date"] = pd.to_datetime(df["date"])
print(df.dtypes)

benchmarks_list = df['name'].unique()

for benchmark in benchmarks_list:
    bench_data = df.loc[df['name'] == benchmark]
    bench_data[["date", "time"]].set_index("date").to_csv(benchmark.replace('/', '_').replace(':', '_')+'.csv')
