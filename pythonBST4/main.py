import sys
from threading import Thread
import time
import threading
import traceback

from PyQt5.QtCore import Qt, QLine
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QVBoxLayout, QPushButton, QMainWindow, QLineEdit, \
    QPlainTextEdit
from PyQt5.QtGui import QPainter, QPen, QBrush, QPalette

from copy import copy


# queue 클래스
class Queue:
    def __init__(self):
        self.queue = list()
        self.printIdx = -1

    def enqueue(self, key):
        self.queue.append(key)

    def dequeue(self):
        self.printIdx += 1
        return self.queue[self.printIdx]
        pass

    def isEmpty(self):
        if self.printIdx < 0:
            idx = 0
        else:
            idx = self.printIdx

        if len(self.queue[idx:-1]) == 0:
            return True
        else:
            return False


# stack 클래스
class Stack:
    def __init__(self):
        self.stack = list()

    def push(self, key):
        self.stack.append(key)

    def pop(self):
        return self.stack.pop(-1)

    def isEmpty(self):
        if len(self.stack) == 0:
            return True
        else:
            return False


# node 이식
class Node:
    def __init__(self, key, myApp):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None

        self.level = 0

        # 버튼을 생성할 위젯
        self.widget = myApp
        # 버튼 객체
        self.square = QPushButton(str(self.key), myApp)
        # self.square.clicked.connect(self.test_delete)
        self.square.move(700, 100)

        # 라인 객체
        self.line = None

    def __del__(self):
        print()

    def addNode(self, key):
        currentNode = self

        while currentNode is not None:
            value = currentNode.key
            if key < value:
                if currentNode.left is None:
                    currentNode.left = Node(key, self.widget)
                    currentNode.left.level = currentNode.level + 1
                    currentNode.left.square.move(
                        currentNode.square.geometry().x() - 50 * (6 - (currentNode.left.level - 1) * 2),
                        currentNode.square.geometry().center().y() + 50)
                    currentNode.left.parent = currentNode
                    self.line = QLine(currentNode.square.geometry().center().x(),
                                      currentNode.square.geometry().center().y(),
                                      currentNode.square.geometry().center().x() - 50 * (
                                              6 - (currentNode.left.level - 1) * 2),
                                      currentNode.square.geometry().center().y() + 50)
                    self.widget.lines.append(self.line)
                    self.widget.repaint()
                    break
                currentNode = currentNode.left

            elif key > value:
                if currentNode.right is None:
                    currentNode.right = Node(key, self.widget)
                    currentNode.right.level = currentNode.level + 1
                    currentNode.right.square.move(
                        currentNode.square.geometry().center().x() + 50 * (6 - (currentNode.right.level - 1) * 2),
                        currentNode.square.geometry().center().y() + 50)
                    currentNode.right.parent = currentNode
                    self.line = QLine(currentNode.square.geometry().center().x(),
                                      currentNode.square.geometry().center().y(),
                                      currentNode.square.geometry().center().x() + 50 * (
                                              6 - (currentNode.right.level - 1) * 2),
                                      currentNode.square.geometry().center().y() + 50)
                    self.widget.lines.append(self.line)
                    self.widget.repaint()
                    break
                currentNode = currentNode.right

    def searchNode(self, key):
        currentNode = self

        while currentNode is not None:
            time.sleep(1)
            if currentNode is not None:
                currentNode.square.setStyleSheet("color: red;")
                self.widget.repaint()

            value = currentNode.key
            if key < value:
                currentNode = currentNode.left

            elif key > value:
                currentNode = currentNode.right

            elif key == value:
                break

        if currentNode is None:
            print('search failed')

    def reset(self, node):
        currentNode = node
        if currentNode is None:
            return
        currentNode.square.setStyleSheet("color: black;")
        self.reset(currentNode.right)
        self.reset(currentNode.left)

    def delete(self, key):

        currentNode = self

        while currentNode is not None:
            time.sleep(1)
            if currentNode is not None:
                currentNode.square.setStyleSheet("color: red;")
                self.widget.repaint()

            value = currentNode.key
            if key < value:
                currentNode = currentNode.left

            elif key > value:
                currentNode = currentNode.right

            elif key == value:
                alter = self.find_alter(currentNode)
                if alter is not None:
                    # alter.square.move(currentNode.square.geometry().x(),
                    #                  currentNode.square.geometry().y())
                    # alter.right = currentNode.right
                    # alter.left = currentNode.left
                    currentNode.key = alter.key
                    currentNode.square.setText(str(currentNode.key))
                    alter.square.hide()
                    # alter.line.setLine(0, 0, 0, 0)


                else:
                    if currentNode.parent is None:
                        del currentNode
                        pass

                    else:
                        currentNode.line.setLine(0, 0, 0, 0)
                        currentNode.square.hide()
                        if currentNode.parent.right.key == currentNode.key:
                            currentNode.parent.right = None

                            pass
                        elif currentNode.parent.left.key == currentNode.key:
                            currentNode.parent.left = None
                            pass

                break

    def find_alter(self, node):
        current = node

        if current.left is not None:
            current = current.left
            while current is not None:
                if current.right is None:
                    break
                current = current.right

            current.parent.right = None

            pass

        elif current.right is not None:
            current = current.right
            while current is not None:
                if current.left is None:
                    break
                current = current.left

            current.parent.left = None
            pass

        else:
            current = None

        return current


# BST 이식
class BinarySearchTree:
    def __init__(self, myApp):
        self.pause = False
        self.resume = True

        self.widget = myApp
        self.root = None

    def addNode(self, value):
        if not self.root:
            self.root = Node(value, self.widget)
        else:
            self.root.addNode(value)

    def searchNode(self, value):
        self.root.searchNode(int(value))
        pass

    def delete(self, key):
        if self.root.left is None and self.root.right is None:
            self.root.square.hide()
        else:
            self.root.delete(key)

        pass

    def reset(self, node):
        self.root.reset(self.root)
        pass

    # 트리의 순회
    def traversal_preorder(self, node):
        if node is not None:
            # while loop를 이용한 정지
            while self.pause:
                print('in pause')
                time.sleep(1)

            if not self.resume:
                self.pause = True

            node.square.setStyleSheet("color: red;")
            # self.repaint()
            # self.widget.te_step.setText(str(node.key))
            time.sleep(1)
            node.square.setStyleSheet("color: black;")
            # self.repaint()
            self.traversal_preorder(node.left)
            self.traversal_preorder(node.right)
            # time.sleep(3)

        return

    def traversal_inorder(self, node):
        if node is not None:
            self.traversal_inorder(node.left)

            node.square.setStyleSheet("color: red;")
            self.widget.repaint()
            time.sleep(1)
            node.square.setStyleSheet("color: black;")
            self.widget.repaint()

            self.traversal_inorder(node.right)

    def traversal_postorder(self, node):
        if node is not None:
            self.traversal_postorder(node.left)

            self.traversal_postorder(node.right)
            node.square.setStyleSheet("color: red;")
            self.widget.repaint()
            time.sleep(1)
            node.square.setStyleSheet("color: black;")
            self.widget.repaint()

    # while문을 이용한 BFS
    def bfs(self):
        my_Queue = Queue()
        my_Queue.enqueue(self.root)

        while my_Queue.isEmpty() is not None:
            current = my_Queue.dequeue()
            current.square.setStyleSheet("color: red;")
            self.widget.te_record.setText(self.widget.te_record.text() + " " + str(current.key))
            time.sleep(1)
            current.square.setStyleSheet("color: black;")
            if current.left is not None:
                my_Queue.enqueue(current.left)

            if current.right is not None:
                my_Queue.enqueue(current.right)

    # while문을 이용한 DFS
    def dfs(self):
        my_Stack = Stack()
        my_Stack.push(self.root)

        while my_Stack.isEmpty() is not None:
            current = my_Stack.pop()
            current.square.setStyleSheet("color: red;")
            self.widget.te_record.setText(self.widget.te_record.text() + " " + str(current.key))
            time.sleep(1)
            current.square.setStyleSheet("color: black;")
            if current.right is not None:
                my_Stack.push(current.right)

            if current.left is not None:
                my_Stack.push(current.left)


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        # BST 생성
        self.bst = BinarySearchTree(self)

        self.te = QLineEdit(self)
        self.lbl1 = QLabel('Enter your sentence:')
        self.btn_add = QPushButton('ADD', self)
        self.lbl2 = QLabel('The number of words is 0')
        self.btnCount = 0
        self.btn_inOrder = QPushButton('inOrder', self)
        self.btn_preOrder = QPushButton('preOrder', self)
        self.btn_postOrder = QPushButton('postOrder', self)
        self.btn_search = QPushButton('search', self)
        self.btn_reset = QPushButton('reset', self)
        self.btn_delete = QPushButton('delete', self)

        # 스텝별 이동을 위한 리스트와 인덱스
        self.stepList = list()
        self.stepIdx = -1

        # bfs와 dfs
        self.btn_bfs = QPushButton('BFS', self)
        self.btn_dfs = QPushButton('DFS', self)

        # 순회 기록 텍스트박스
        self.te_record = QLineEdit(self)

        # 커스텀 함수용 함수 작성창
        self.text_custom = QPlainTextEdit(self)
        self.btn_confirm = QPushButton('confirm', self)

        # # pause와 resume
        self.pause = False
        # self.resume = True
        self.btn_pause = QPushButton('pause', self)
        self.btn_resume = QPushButton('resume', self)
        # # self.t_preorder.setDaemon(True)
        #
        # # 스텝별 이동 구현용 컨트롤
        # self.btn_trav_step_preOrder = QPushButton('preOrder_step', self)
        # self.te_step = QLineEdit(self)
        # self.btn_next = QPushButton('next step', self)
        # self.btn_prev = QPushButton('prev step', self)

        # 라인 리스트
        self.lines = list()

        self.initUI()

    def initUI(self):
        self.te.move(20, 20)
        self.te.resize(self.btn_add.sizeHint())
        self.te.returnPressed.connect(self.add_node)

        # 노드 추가 버튼
        self.btn_add.move(100, 20)
        self.btn_add.resize(self.btn_add.sizeHint())
        self.btn_add.clicked.connect(self.add_node)

        # bfs, dfs 버늩
        self.btn_bfs.move(10, 50)
        self.btn_bfs.resize(self.btn_add.sizeHint())
        self.btn_bfs.clicked.connect(self.BFS)
        self.btn_dfs.move(85, 50)
        self.btn_dfs.resize(self.btn_add.sizeHint())
        self.btn_dfs.clicked.connect(self.DFS)

        # 순회 버튼(inOrder)
        self.btn_inOrder.move(200, 20)
        self.btn_inOrder.resize(self.btn_add.sizeHint())
        self.btn_inOrder.clicked.connect(self.traversal_inorder_root)

        # 순회 버튼(preOrder)
        self.btn_preOrder.move(300, 20)
        self.btn_preOrder.resize(self.btn_add.sizeHint())
        self.btn_preOrder.clicked.connect(self.traversal_preorder_root)

        # 순회 버튼(postOrder)
        self.btn_postOrder.move(400, 20)
        self.btn_postOrder.resize(self.btn_add.sizeHint())
        self.btn_postOrder.clicked.connect(self.traversal_postorder_root)

        # 탐색 버튼
        self.btn_search.move(500, 20)
        self.btn_search.resize(self.btn_add.sizeHint())
        self.btn_search.clicked.connect(self.search_te)

        # 초기화 버튼
        self.btn_reset.move(600, 20)
        self.btn_reset.resize(self.btn_add.sizeHint())
        self.btn_reset.clicked.connect(self.reset_BST)

        # 노드 삭제 버튼
        self.btn_delete.move(700, 20)
        self.btn_delete.resize(self.btn_add.sizeHint())
        self.btn_delete.clicked.connect(self.delete_te)

        # 순회 기록 텍스트박스
        self.te_record.move(50, 950)
        self.te_record.resize(1400, 30)

        # 커스텀 함수용 함수 작성창
        self.text_custom.move(50, 500)
        self.text_custom.resize(1400, 400)

        self.btn_confirm.move(50, 915)
        self.btn_confirm.clicked.connect(self.runCustom)

        # pause, resume 버튼 이동
        self.btn_pause.move(270, 45)
        self.btn_pause.clicked.connect(self.active_pause)
        self.btn_resume.move(330, 45)
        self.btn_resume.clicked.connect(self.active_resume)

        # 스텝별 이동 구현용 컨트롤 이동
        # self.btn_trav_step_preOrder.move(800, 5)
        # self.btn_trav_step_preOrder.clicked.connect(self.traversal_preorder_root_step)
        # self.te_step.move(800, 30)
        # self.btn_next.move(800, 55)
        # self.btn_next.clicked.connect(self.step_next)
        # self.btn_prev.move(875, 55)
        # self.btn_prev.clicked.connect(self.step_prev)

        self.setWindowTitle('QTextEdit')
        self.setGeometry(100, 100, 1500, 1000)
        self.show()

    # pause, resume 버튼 동작
    def active_pause(self):
        self.pause = True

    def active_resume(self):
        self.pause = False

    def debugPoint(self):
        while self.pause == True:
            time.sleep(1)

    def runCustom(self):
        self.te_record.clear()
        active_thread = threading.Thread(target=self.customThread)
        active_thread.start()

    def customThread(self):
        try:
            customCode = self.text_custom.toPlainText()
            customCode = customCode.replace("wait", "self.pause=True\nself.debugPoint()")
            exec(customCode)
            print()
        except Exception:
            self.te_record.setText(traceback.format_exc())
        finally:
            pass

    def add_node(self):
        key = int(self.te.text())
        self.bst.addNode(key)
        self.draw_BST(self.bst.root)
        self.te.clear()
        pass

    def reset_BST(self):
        node = self.bst.root
        self.bst.reset(node)
        pass

    def delete_te(self):
        key = int(self.te.text())
        self.bst.delete(key)
        pass

    def draw_BST(self, node):
        currentNode = node
        if currentNode is not None:
            currentNode.square.show()

        if currentNode.left is not None:
            self.draw_BST(currentNode.left)

        if currentNode.right is not None:
            self.draw_BST(currentNode.right)

    def search_te(self):
        key = self.te.text()
        self.bst.searchNode(key)
        pass

    def traversal_preorder_root(self):
        node = self.bst.root
        active_thread = threading.Thread(target=self.bst.traversal_preorder, args=(node,))
        # self.traversal_preorder(node)
        active_thread.start()
        # active_thread.join()
        return

    def BFS(self):
        self.te_record.clear()
        active_thread = threading.Thread(target=self.bst.bfs)
        # self.traversal_preorder(node)
        active_thread.start()
        # active_thread.join()
        return

    def DFS(self):
        self.te_record.clear()
        active_thread = threading.Thread(target=self.bst.dfs)
        # self.traversal_preorder(node)
        active_thread.start()
        # active_thread.join()
        pass

    # def traversal_preorder_root_step(self):
    #     node = self.bst.root
    #     self.traversal_preorder_step(node)
    #     pass
    #
    def traversal_inorder_root(self):
        node = self.bst.root
        self.traversal_inorder(node)
        pass

    def traversal_postorder_root(self):
        node = self.bst.root
        self.traversal_postorder(node)
        return

    # def traversal_preorder_step(self, node):
    #     if node is not None:
    #         self.stepList.append(node)
    #         self.traversal_preorder_step(node.left)
    #         self.traversal_preorder_step(node.right)
    #
    # def step_next(self):
    #     self.stepIdx += 1
    #     self.stepList[self.stepIdx].square.setStyleSheet("color: red;")
    #     self.repaint()
    #
    # def step_prev(self):
    #     self.stepList[self.stepIdx].square.setStyleSheet("color: black;")
    #     self.stepIdx -= 1
    #     self.repaint()

    def paintEvent(self, event):
        pen = QPen()
        brush = QBrush(Qt.darkCyan, Qt.Dense7Pattern)
        painter = QPainter(self)
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)

        for line in self.lines:
            painter.drawLine(line)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
