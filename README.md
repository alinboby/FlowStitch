# FlowStitch
A forensic tool to extract and reconstruct fragmented HTTP image data from pcap files using content-range headers.

### Details
Python program named FlowStitch, version 1.0.0, developed by HxN0n3.

    Takes 3 inputs from the user:
        PCAP filename (e.g., forensic.pcap)
        HTTP content type (e.g., image/jpeg)
        Output image filename (e.g., final.jpeg)
    Extracts HTTP image fragments using http.content_range
    Sorts fragments by byte position
    Merges hex data and writes as binary image

### Installation
    git clone https://github.com/alinboby/FlowStitch/
    pip install pyshark
    cd FlowStitch
    
### Run 
![6](https://github.com/user-attachments/assets/47a60b2c-4903-436e-a96d-0f336d709ea3)


### Sample file
forensic.pcap

### output after running program
![output](https://github.com/user-attachments/assets/662eda39-846f-42bc-b4d3-ada0cdd8e3a4)
