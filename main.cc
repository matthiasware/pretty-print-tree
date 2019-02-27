#include <iostream>
#include <string>
#include <vector>

struct Node {
  Node(std::string name, Node *left=nullptr, Node *right=nullptr)
      : name_{name}, left_{left}, right_{right} {};
  std::string name_;
  Node *left_;
  Node *right_;

  void del()
  {
    std::cout << "Delete " << name_ << std::endl;
    if(left_)
    {
      left_->del();
      delete left_;
    }
    if(right_)
    {
      right_->del();
      delete right_;
    }
  }
};
void print_preorder(Node *n, std::string ident)
{
  if(n)
  {
    std::cout << ident << "-" << n->name_ << std::endl;
    print_preorder(n->left_, ident + " |");
    print_preorder(n->right_, ident + " |");
  }
}

int depth(Node *n)
{
  if(n != nullptr)
    return 1 + std::max(depth(n->left_), depth(n->right_));
  return 0;
}

int tokenMaxWidth(Node *n)
{
  if(n != nullptr)
    return std::max<int>(n->name_.length(), std::max(tokenMaxWidth(n->left_), tokenMaxWidth(n->right_)));
  return 0;
}

std::string padToken(std::string token, int width)
{
  if(token.length() < width)
  {
    int diff = width - token.length();
    int pad = diff / 2;
    token = std::string(pad, ' ') + token + std::string(pad, ' ');
    if(pad % 2 == 1)
      token += " ";
    // 1 2 3 4 5
  }
  return token;
}


int main() {
  Node root("+",
            new Node("*",
                     new Node("x"),
                     new Node("2")),
            new Node("sin", nullptr, new Node("*", new Node("x"), new Node("4"))));
  Node *n = &root;

  // start algo
  int d = depth(n) - 1;
  int token_width = tokenMaxWidth(n);
  int token_abs_width = token_width + 2;
  int max_leaves = 1 << d;

  std::string result{""};

  std::vector<Node*>  nodes{n};

  for(int e=0; e<=d; ++e)
  {
    int ident = ((2 << (d - e)) - 1) * token_abs_width;
    int node_distance = ((2 << (d - e + 1)) - 1) * token_abs_width;

    std::string line = std::string(ident, ' ');
    std::string previous_line = "";
    std::vector<Node*> nodes_new;

    for(int i=0; i<nodes.size(); ++i)
    {
      std::string s = nodes[i]->name_;
      bool empty = (s == "") ? true : false;
      if(empty)
      {
        s = std::string(token_abs_width, ' ');
      }
      else
      {
        s = "(" + padToken(s, token_width) + ")";
      }
      line.append(s);
      line.append(std::string(node_distance, ' '));
      if(nodes[i]->left_)
        nodes_new.push_back(nodes[i]->left_);
      else
        nodes_new.push_back(new Node(""));
      if(nodes[i]->right_)
        nodes_new.push_back(nodes[i]->right_);
      else
        nodes_new.push_back(new Node(""));
    }
    line += "\n";
    result += line;
    nodes = nodes_new;
  }
  std::cout << result << std::endl;
}