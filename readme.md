
# Drawing A Binary Tree In Console
Given a binary tree, where a node can have 0, 1, or 2 children. E.g. consider the following expression:
```sh
	ln(x) + 3 * sin(x + y)
```
The expression can be represented by a binary expression tree: 

```
tree = Node("*",
             Node("+",
                  Node("ln",
                       Node("x")),
                  Node("3")),
             Node("sin",
                  Node("+",
                       Node("x"),
                       Node("y"))))
```

The algorithm creates a 2D char array and  works as follows:
1) Traverse the tree inorder and ennumerate nodes. The index of a node is its x-coordinate. The height of the node represents its y-coordinate.
2) Simplification; If a node has only one child, they can be vertically alligned.
3) Calculate final x-coordinates by taking the token length into account. Calculate final y-coordinates.
4) Drawing arms recursively, starting with the root.

This yields the following result:

```sh
          *          
   ------   ------   
    +          sin   
---   ---            
ln     3        +    
            ---   ---
 x           x     y 
```