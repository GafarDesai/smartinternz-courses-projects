document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("dataForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const formData = {
    source_ip: document.getElementById("source_ip").value,
    destination_ip: document.getElementById("destination_ip").value,
    protocol: document.getElementById("protocol").value,
    packet_size: document.getElementById("packet_size").value,
    bytes_sent: document.getElementById("bytes_sent").value,
    bytes_received: document.getElementById("bytes_received").value,
    flag: document.getElementById("flag").value,
  };

  const btnText = document.getElementById("btnText");
  const spinner = document.getElementById("spinner");
  const outputBox = document.getElementById("outputBox");

  btnText.innerText = "Checking...";
  spinner.style.display = "inline-block";

  fetch("/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(formData),
  })
    .then((res) => res.json())
    .then((data) => {
      const message = data.result || (data.is_anomaly ? "🚨 Anomaly detected!" : "✅ Normal traffic");

      document.getElementById("alertOutput").innerText = message;
      const details = `
Source IP: ${formData.source_ip}
Destination IP: ${formData.destination_ip}
Protocol: ${formData.protocol}
Packet Size: ${formData.packet_size}
Bytes Sent: ${formData.bytes_sent}
Bytes Received: ${formData.bytes_received}
Flag: ${formData.flag}
`;

document.getElementById("alertData").innerText = details;

      
      document.getElementById("customAlert").style.display = "flex";

      btnText.innerText = "Check for Anomaly";
      spinner.style.display = "none";

      document.getElementById("closeAlertBtn").addEventListener("click", () => {
      document.getElementById("customAlert").style.display = "none";
    });
    }).catch((err) => {
      console.error(err);
      document.getElementById("output").innerText = "Prediction failed.";
      outputBox.classList.add("show");
      document.body.classList.add("drawer-open");

      btnText.innerText = "Check for Anomaly";
      spinner.style.display = "none";
    });
});
});

// Close output drawer
document.getElementById("closeOutputBox").addEventListener("click", function () {
  document.getElementById("outputBox").classList.remove("show");
  document.body.classList.remove("drawer-open");
});


document.getElementById("retrainForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const csvFile = document.getElementById("csvFile").files[0];
  const statusDiv = document.getElementById("retrainStatus");

  if (!csvFile) {
    statusDiv.innerText = "Please upload a CSV file.";
    statusDiv.classList.add("text-danger");
    return;
  }

  const formData = new FormData();
  formData.append("file", csvFile);

  statusDiv.innerText = "Retraining in progress...";
  statusDiv.classList.remove("text-danger");
  statusDiv.classList.add("text-warning");

  fetch("/retrain", {
    method: "POST",
    body: formData,
  })
    .then((res) => res.json())
    .then((data) => {
      statusDiv.innerText = data.message || "Retraining complete!";
      statusDiv.classList.remove("text-warning");
      statusDiv.classList.add("text-success");
    })
    .catch((err) => {
      console.error("Retrain Error:", err);
      statusDiv.innerText = "Retraining failed.";
      statusDiv.classList.remove("text-warning");
      statusDiv.classList.add("text-danger");
    });
});


