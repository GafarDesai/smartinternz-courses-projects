import csv
import random
import datetime

# Generate a random IP address
def random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# Create dummy data for one network packet
def generate_packet():
    return {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_ip": random_ip(),
        "destination_ip": random_ip(),
        "protocol": random.choice(["TCP", "UDP", "ICMP"]),
        "packet_size": random.randint(40, 1500),
        "bytes_sent": random.randint(0, 5000),
        "bytes_received": random.randint(0, 5000),
        "flag": random.choice(["SYN", "ACK", "FIN", "RST", ""]),
        "is_anomaly": random.choice([0, 0, 0, 0, 1])  # 20% chance of anomaly
    }

# Generate and write to CSV
def generate_data(file_name="network_traffic.csv", num_rows=1000):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "timestamp", "source_ip", "destination_ip", "protocol",
            "packet_size", "bytes_sent", "bytes_received", "flag", "is_anomaly"
        ])
        writer.writeheader()
        for _ in range(num_rows):
            writer.writerow(generate_packet())

    print(f"{num_rows} rows of data saved to {file_name}")

# Run only if executed directly
if __name__ == "__main__":
    generate_data()
