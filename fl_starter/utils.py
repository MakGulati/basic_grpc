from time import pthread_getcpuclockid
from pyparsing import python_style_comment
import torch

DEVICE = torch.device("cpu")
from collections import OrderedDict
import SimpleNet


def train(net, trainloader, epochs):
    """Train the network on the training set."""
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    net.train()
    for _ in range(epochs):
        for images, labels in trainloader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            optimizer.zero_grad()
            loss = criterion(net(images), labels)
            loss.backward()
            optimizer.step()
    return loss


def test(net, testloader):
    """Validate the network on the entire test set."""
    criterion = torch.nn.CrossEntropyLoss()
    correct, total, loss = 0, 0, 0.0
    net.eval()
    with torch.no_grad():
        for data in testloader:
            images, labels = data[0].to(DEVICE), data[1].to(DEVICE)
            outputs = net(images)
            loss += criterion(outputs, labels).item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    accuracy = correct / total
    return loss, accuracy

    # Unpack the CIFAR-10 dataset partition
    # trainloader, testloader = dataset


class CifarClient:
    def __init__(self, model, trainloader, testloader):
        self.net = model
        self.trainloader = trainloader
        self.testloader = testloader

    def get_parameters(self):
        return [val.cpu().numpy() for _, val in self.net.state_dict().items()]

    def set_parameters(self, parameters):
        params_dict = zip(self.net.state_dict().keys(), parameters)
        state_dict = OrderedDict({k: torch.tensor(v) for k, v in params_dict})
        self.net.load_state_dict(state_dict, strict=True)
        print("set_parameters")

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        train(self.net, self.trainloader, epochs=1)
        print("finished training")
        return self.get_parameters(), len(self.trainloader.dataset), {}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        loss, accuracy = test(self.net, self.testloader)

        return float(loss), len(self.testloader), {"accuracy": float(accuracy)}

    def state_dict_to_json(self, parameters):
        self.set_parameters(parameters)
        torch.save(self.net.state_dict(), "sample.pth")
        return "written to json"
