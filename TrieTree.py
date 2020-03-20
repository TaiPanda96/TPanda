class Node:
    def __init__(self,root):
        self.root          = root
        self.children      = [None] * 26 #alphabet 
        self.left          = None
        self.right         = None 
        self.last_word     = None 

class TrieTree:
    def __init__(self):
        self.root = self.get_node()

    def get_node(self):
        return Node(self)

    def char_index(self,ch):
        return ord(ch) - ord('a')
    
    def insert_key(self,search_element):
        """
        This function does the following:
        1) Define the starting search term, which is the root node.
        2) Iterater through the search_key_term user provides. 
           For each element of the key term, identify if trie-tree 
           has this element already.
             A) If search term already exists, then match the starting search term
                to the children element that was found in trie-tree
             B) Otherwise, insert this element into the trie-tree as a new child node.
        3) Update the 'End Word' flag upon completion of the traversal, saying we've reached the last possible node in the trie-structure.
        """
        start = self.root
        for element in range(len(search_element)):
            element = self.char_index(ch=search_element[element])
  
            if not start.children[element]:
                start.children[element] = self.get_node()
            else:    
                start = start.children[element]

            # Mark last node in the search term as leaf node:
            start.last_word = True 
    
    def search(self,search_element):
        start = self.root
        for element in range(len(search_element)):
            element = self.char_index(search_element[element])

            if not start.children[element]:
                return False
            else:
                return start.children[element] != None and start.last_word
 
        
def main():
    # Input keys (use only 'a' through 'z' and lower case) 
    search_element = ["homework","housing","hot","home","the","these","a","their","them","any","plaza","penthouse"] 
    output = ["Not present in trie", "Present in trie"] 
  
    #Trie object 
    t = TrieTree() 
  
    # Construct trie 
    for element in search_element: 
        t.insert_key(element)
  
    # Search for different keys 
    print("{} ----> {}".format("pizza",      output[t.search("pizza")])) 
    print("{} ----> {}".format("pension",    output[t.search("pension")])) 
    print("{} ----> {}".format("that",       output[t.search("that")])) 
    print("{} ----> {}".format("thaw",       output[t.search("thaw")]))
    print("{} ----> {}".format("home",       output[t.search("home")])) 
    print("{} ----> {}".format("housing",    output[t.search("housing")]))
    print("{} ----> {}".format("hot",        output[t.search("hot")]))
    print("{} ----> {}".format("homey",      output[t.search("homey")]))
    print("search element list --->",search_element)


if __name__ =="__main__":
    main()
 