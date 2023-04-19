#!/usr/local/cs/bin/python3
# Keep the function signature,
# but replace its body with your implementation.
#
# Note that this is the driver function.
# Please write a well-structured implemention by creating other functions outside of this one,
# each of which has a designated purpose.
#
# As a good programming practice,
# please do not use any script-level variables that are modifiable.
# This is because those variables live on forever once the script is imported,
# and the changes to them will persist across different invocations of the imported functions.
import os, sys, zlib

class CommitNode:
    def __init__(self, commit_hash):
        """
        :type commit_hash: str
        """
        self.commit_hash = commit_hash
        self.parents = set()
        self.children = set()
        
    # Override default equality to be based on commit_hash
    def __eq__(self, other):
        return isinstance(other, CommitNode) and self.commit_hash == other.commit_hash
    
    # Override default equality to be based on commit_hash
    def __hash__(self):
        return hash(self.commit_hash)
    
    # Add a parent node method
    def add_parent(self, commit_hash):
        self.parents.add(commit_hash)
        
    # Add a child node method
    def add_child(self, commit_hash):
        self.children.add(commit_hash)
    
    # Print out current hash
    def print_hash(self):
        print("My hash:", self.commit_hash)
    
    # Print out parent hashes
    def print_parent_hash(self):
        for parent in self.parents:
            print("Parent: ", parent)
        
    # Print out children hashes
    def print_child_hash(self):
        for child in self.children:
            print("Child: ", child)

# Searches for a ".git" file in current + parent directories
# Returns the absolute path of the .git directory
def git_search(start_path):
    if start_path == "/":
        print("Not inside a Git Repository", file=sys.stderr)
        sys.exit(1)
    if ".git" in os.listdir(start_path):
        return os.path.join(start_path, ".git")

    return git_search(os.path.abspath(os.path.join(start_path, os.pardir)))

# Returns absolute paths of all branches in .git directory
def get_branch(git_path):
    dir_list = []
    branch_list = []
    # Adds top level branches and accounts for branches with / in them
    for branch in os.listdir(os.path.join(git_path, "refs/heads")):
        if os.path.isdir(os.path.join(git_path, "refs/heads/{}".format(branch))):
            dir_list.append(os.path.join(git_path, "refs/heads/{}".format(branch)))
        else:
            branch_list.append(os.path.join(git_path, "refs/heads/{}".format(branch)))
    # Checks all / cases and resolves them
    while dir_list:
        for potential_branch in os.listdir(dir_list[-1]):
            if os.path.isdir(os.path.join(dir_list[-1], potential_branch)):
                tmp = dir_list[-1]
                dir_list.pop()
                dir_list.append(os.path.join(tmp, potential_branch))
            else:
                branch_list.append(os.path.join(dir_list[-1], potential_branch))
                dir_list.pop()
            
    return branch_list

# Returns array of commit checksums given paths to files
def get_commits(abs_paths):
    commit_list = []
    for path in abs_paths:
        with open(path, 'r') as file:
            commit_list.append(file.read().rstrip("\n"))
    return commit_list

# Returns a list of decoded contents given a list of commits and the abs path to .git
# Decoded: Decompressed byte contents of folders using zlib
def decode(list_of_commits, git_path):
    decoded_contents = []
    for commit in list_of_commits:
        dir = commit[:2] 
        entry = commit[2:]
        filepath = os.path.join(git_path, "objects/{}/{}".format(dir, entry)) # filepath should be correct according to spec
        with open(filepath, "rb") as file:
            contents = zlib.decompress(file.read())
        decoded_contents.append(contents.decode('utf-8'))
    return decoded_contents

# Returns the parent hashes given a single commit 
def parent_decode(commit, git_path):
    parents = []
    dir = commit[:2]
    entry = commit[2:]
    filepath = os.path.join(git_path, "objects/{}/{}".format(dir, entry))
    with open(filepath, "rb") as file:
        contents = zlib.decompress(file.read())
        contents = contents.decode("utf-8")
    for category in contents.split("\n"):
        if category.split(" ")[0] == "parent":
            parent = category.split(" ")[1]
            parents.append(parent)
    return parents

# Returns a commit graph (in a set data structure) given decoded contents and a list of currently tracked commits
def create_commit_graph(list_of_decoded_contents, list_of_commits, git_path):
    return_dict = {}
    stack = []
    # Adds all branch commit hashes to the return dictionary + stack
    for branch_commit in list_of_commits:
        stack.append(branch_commit)
        return_dict[branch_commit] = CommitNode(branch_commit)
    # Adds all parent commit hashes of the branch commits to the return dictionary + stack
    for entry in list_of_decoded_contents:
        for category in entry.split("\n"):
            if category.split(" ")[0] == "parent":
                commit = category.split(" ")[1]
                stack.append(commit)
                return_dict[commit] = CommitNode(commit)
    
    # Performs DFS on commit stack
    while stack:
        cur_commit = stack.pop()
        childref = CommitNode(cur_commit)
        # If the current commit is not in the return_dict, add it to the return_dict
        if cur_commit not in return_dict:
            return_dict[cur_commit] = childref
        else: # If the current commit is in the return_dict, take its assigned val in the dict
            childref = return_dict[cur_commit]
            
        # Iterate through all parent commits of the current commit
        for parent in parent_decode(cur_commit, git_path):
            parentref = CommitNode(parent)
            parentref.add_child(cur_commit) # Create a parent node and make the current commit its child
            childref.add_parent(parent) # Add the parent to the cur_commit child node
            # Adds the parent to the return_dict if not in the dict
            if parent not in return_dict:
                return_dict[parent] = parentref 
            else: # Else updates the element that is in the dict
                tmp = return_dict[parent] 
                tmp.add_child(cur_commit)
                return_dict[parent] = tmp
            stack.append(parent)
                
        # Update current commit in the dictionary
        return_dict[cur_commit] = childref
    
    return_nodes = []
    for key in return_dict:
        return_nodes.append(return_dict[key])
    
    return return_nodes     

# Performs a toposort given a list of nodes from the commit graph
def toposort(node_list):
    stack = []
    visit_list = [0] * len(node_list) # Creates corresponding list of unvisited nodes
    
    # Iterate through all nodes and perform toposort
    for i, node in enumerate(node_list):
        if (visit_list[i] == 0):
            dfs(i, node, node_list, visit_list, stack)
    
    # Return in order from least to greatest
    return stack
            
# Utility function for toposort() function which modifies stack and visit_list using DFS
def dfs(index, node, node_list, visit_list, stack):
    visit_list[index] = 1
    
    # Iterate through children in passed in node (CHILD OF STRING TYPE)
    # Sorting children to make set deterministic and result uniform
    for child in sorted(node.children):
        index_in_original = None
        node_in_original = None
        # Checks all nodes in node_list again for where the child resides
        for i, node in enumerate(node_list):
            if child == node.commit_hash:
                index_in_original = i # Store index of child commit in original node_list
                node_in_original = node_list[i] # Store actual node object of child in original node_list
                break
        # If child is unvisited, then recurse this function again with the child node
        if (visit_list[index_in_original] == 0):
            dfs(index_in_original, node_in_original, node_list, visit_list, stack)
    
    stack.append(node_list[index]) # Push to stack when all children have been considered
    
# Utility function to create dictionary that maps commits to branch heads
# Also sorts branches in lexicographical order once all have been added
def branch_commit_relations(branch_paths, commit_list):
    return_dict = {}
    for i in range(len(branch_paths)):
        # Extracts branch name from end of absolute path URL
        branch_name = branch_paths[i][branch_paths[i].index("heads") + 6 :]
        if commit_list[i] in return_dict:
            return_dict[commit_list[i]].append(branch_name)
        else:
            return_dict[commit_list[i]] = [branch_name]
       
    # Sorts branch names in lexicographical order
    for key in return_dict:
        return_dict[key] = sorted(return_dict[key])
   
    return return_dict

# Prints the graph given the topologically sorted commits and the commit-branch name relationships
def print_graph(topologically_sorted_commits, branch_name_to_commit_dict):
    sticky_end = False # Variable that stores state of sticky end
    
    # Iterates through all nodes within topologically_sorted_commits
    for i, node in enumerate(topologically_sorted_commits):
        # If a sticky end has just been inserted, create a sticky start
        if (sticky_end):
            sticky_end = False
            set_counter = 0
            
            # If there's children to be printed, do the following body
            if len(node.children) != 0:
                print('=', end="")
                
                # Print children with whitespace
                for child in node.children:
                    if set_counter + 1 == len(node.children):
                        print(child)
                    else:
                        print(child, end=" ")
                    set_counter += 1
            else:
                print('=')
        
        # Prints the associated branch names with each commit
        if node.commit_hash in branch_name_to_commit_dict:
            print(node.commit_hash, end=" ")
            for j, branch_name in enumerate(branch_name_to_commit_dict[node.commit_hash]):
                if j + 1 == len(branch_name_to_commit_dict[node.commit_hash]):
                    print(branch_name)
                else:
                    print(branch_name, end=" ")
        else:
            print(node.commit_hash)
   
        # Checks if next commit is a direct parent of current commit and inserts sticky end if not
        if (i + 1 < len(topologically_sorted_commits)) and (topologically_sorted_commits[i + 1].commit_hash not in topologically_sorted_commits[i].parents):
            sticky_end = True
            set_counter = 0
            
            # If there's parents to be printed, do the following body
            if len(node.parents) != 0:
                
                # Print parents with newlines
                for parent in node.parents:
                    if set_counter + 1 == len(node.parents):
                        print(parent + "=" + '\n')
                    else:
                        print(parent)
                    set_counter += 1
            else:
                print('=' + '\n')
        

def topo_order_commits():
    git_dir = git_search(os.getcwd())
    branch_paths = get_branch(git_dir)
    commit_list = get_commits(branch_paths)
    decoded_contents = decode(commit_list, git_dir)
    graph = create_commit_graph(decoded_contents, commit_list, git_dir)
    topo_sorted_commits = toposort(graph)
    branch_commit_relation = branch_commit_relations(branch_paths, commit_list)
    print_graph(topo_sorted_commits, branch_commit_relation)   
        
if __name__ == '__main__':
    topo_order_commits()
    
### HOW I USED STRACE TO VERIFY NO SYSTEM CALLS WERE USED ###
# I first called strace -f -o res.txt python3 topo_order_commits.py
# The above command took the list of processes and put it into a file called res.txt
# I then did cat res.txt | grep "git" to verify I did not call any git commands
# I then did emacs res.txt and used the I-search functionality to manually search for Linux commands and came across none
