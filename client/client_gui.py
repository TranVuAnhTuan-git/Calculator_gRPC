import tkinter as tk
from tkinter import messagebox
import grpc
import calculator_pb2
import calculator_pb2_grpc

class CalculatorClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("Calculator gRPC Client")

        tk.Label(master, text="Số 1:").grid(row=0, column=0)
        tk.Label(master, text="Số 2:").grid(row=1, column=0)
        tk.Label(master, text="Kết quả:").grid(row=2, column=0)

        self.num1 = tk.Entry(master)
        self.num2 = tk.Entry(master)
        self.result = tk.Entry(master)

        self.num1.grid(row=0, column=1)
        self.num2.grid(row=1, column=1)
        self.result.grid(row=2, column=1)

        tk.Button(master, text="Cộng", command=self.add).grid(row=3, column=0)
        tk.Button(master, text="Trừ", command=self.subtract).grid(row=3, column=1)
        tk.Button(master, text="Nhân", command=self.multiply).grid(row=4, column=0)
        tk.Button(master, text="Chia", command=self.divide).grid(row=4, column=1)

        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = calculator_pb2_grpc.CalculatorServiceStub(self.channel)

    def add(self):
        self.calculate("add")

    def subtract(self):
        self.calculate("subtract")

    def multiply(self):
        self.calculate("multiply")

    def divide(self):
        self.calculate("divide")

    def calculate(self, op):
        try:
            num1 = float(self.num1.get())
            num2 = float(self.num2.get())
            req = calculator_pb2.CalcRequest(num1=num1, num2=num2)

            if op == "add":
                reply = self.stub.Add(req)
            elif op == "subtract":
                reply = self.stub.Subtract(req)
            elif op == "multiply":
                reply = self.stub.Multiply(req)
            elif op == "divide":
                reply = self.stub.Divide(req)

            self.result.delete(0, tk.END)
            self.result.insert(0, str(reply.result))

        except grpc.RpcError as e:
            messagebox.showerror("Lỗi", e.details())
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")

if __name__ == "__main__":
    root = tk.Tk()
    gui = CalculatorClientGUI(root)
    root.mainloop()
