
from .data_receiver import DataReceiver
from .data_sender import DataSender

if __name__ == '__main__':
    receiver = DataReceiver()
    receiver.start_receiving()
