import pandas as pd
import random
import datetime

def generate_dummy_data_expanded(num_entries=100):
    data = []
    now = datetime.datetime.now()

    for _ in range(num_entries):
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        can_data = [random.randint(0, 255) for _ in range(8)]  # 8 random bytes
        data.append([timestamp] + can_data)
        
        # Increment time by a random interval between 0 and 5 seconds
        now += datetime.timedelta(seconds=random.randint(0, 5))

    columns = ["Timestamp"] + [f"Byte_{i+1}" for i in range(8)]
    df = pd.DataFrame(data, columns=columns)
    return df

# Generate expanded dummy data
df_dummy_expanded = generate_dummy_data_expanded(100)

# Save to CSV file
csv_filename_expanded = "dummy_can_data_expanded.csv"
df_dummy_expanded.to_csv(csv_filename_expanded, index=False)
