# Sub-class for linked list
class node:
    def __init__(self,data=None):
        self.data = data
        self.next = None 


class linked_list:
    # start with head node, which contains no data. 
    def __init__(self):
        self.head = node()

        # Node Adder
    def append(self,data):
        # instantiate the next node with node class data object
        next_node = node(data)
        # insertion is from left to right, which means we start with head node (no data)
        current_node = self.head 
        # while the node in question is not the head node or tail node:
        # current_node inherits the 'next' node object in the node class 
        # current_node.next is defined as the 'next' node.
        while current_node.next != None:
            current_node = current_node.next
        current_node.next = next_node

        # Utility Function to Calculate Length of Linked List
    def length(self):
        current_node = self.head
        # counter for visited indices
        visited_index = 0 
        while current_node.next != None:
             visited_index +=1
             current_node = current_node.next
        return visited_index

    def display(self):
        elements_seen = [] 
        current_node = self.head 
        while current_node.next != None:
            current_node = current_node.next 
            elements_seen.append(current_node.data)
        print (elements_seen)

    def search_by_index(self,x):
        if x >= self.length():
            print('the index you are fetching exceeds length of the linked list')
            return None 
        
        current_node = self.head 
        current_index = 0 

        while True:
            current_node = current_node.next
            if current_index == x:
                return print(current_node.data)
            current_index +=1
        return print(current_node.data)


    def search_by_value(self,value):
        current_node = self.head
        current_index = 0 
        if current_index>= self.length():
            print('the index you are fetching exceeds length of hte linked list')
            return None 
    
        while True: 
            current_node = current_node.next 
            if current_node.data == value: 
                return print(current_node.data)
        current_index +=1
        


    def delete_by_index(self,x):
        if x>= self.length():
            print('the index you are fetching exceeds length of the linked list')
            return None 

        current_node = self.head
        target_index = 0

        while True:
            last_node = current_node 
            current_node = current_node.next 
            if target_index == x: 
                return last_node.next == current_node.next
            target_index +=1


# Testing the linked list 
test_linked_list = linked_list()
test_linked_list.append(1)
test_linked_list.append(2)
test_linked_list.append(3) 
test_linked_list.append(4)
test_linked_list.append(5)
test_linked_list.append(5)
test_linked_list.append(10)
test_linked_list.append(20)
test_linked_list.append(121)
test_linked_list.append(87)
test_linked_list.append(64)
test_linked_list.append(11)
test_linked_list.append(27)

test_linked_list.display()
test_linked_list.search_by_index(7)
test_linked_list.search_by_value(20)
print('The length of the linked list is =',test_linked_list.length())
        


    