
from data_receiver import DataReceiver
from data_sender import DataSender

if __name__ == '__main__':
    receiver = DataReceiver()
    receiver.start_receiving()

    # sender = DataSender("25.119.38.155", 8080)
    # sender.send_data("Test message".encode())
