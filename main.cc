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

int depth(Node *n)
{
  if(n != nullptr)
    return 1 + std::max(depth(n->left_), depth(n->right_));
  return 0;
}

int maxtoken(Node *n)
{
  if(n != nullptr)
    return std::max<int>(n->name_.length(), std::max(maxtoken(n->left_), maxtoken(n->right_)));
  return 0;
}

void print_preorder(Node *n, std::string ident)
{
  if(n)
  {
    std::cout << ident << "-" << n->name_ << std::endl;
    print_preorder(n->left_, ident + " |");
    print_preorder(n->right_, ident + " |");
  }
}

int calcTokenWidth(Node *n)
{
  int maxlength = maxtoken(n) + 2;
  return maxlength;
}

std::string padToken(std::string token, int width)
{
  token = "(" + token + ")";
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
  Node root("a",
            new Node("b",
                     new Node("c"),
                     new Node("d")),
            new Node("e", nullptr, new Node("g", new Node("h"))));
  Node *n = &root;
  int d = depth(n) - 1;
  int m = maxtoken(n);
  int max_leaves = 1 << d;

  // std::cout << "Depth:  " << d << std::endl;
  // std::cout << "Leaves: " << max_leaves << std::endl;

  int maxlength = maxtoken(n) + 2;
  std::string result{""};
  std::vector<Node*>  nodes{n};
  for(int e=0; e<=d; ++e)
  {
    int ident = (2 << (d - e)) - 1;
    ident *= maxlength;
    int node_distance = (2 << (d - e + 1)) - 1;
    node_distance *= maxlength;
    std::string line = std::string(ident, ' ');
    int next_line_ident = ident / 2;
    // std::string next_line = std::string(next_line_ident, ' ');
    std::vector<Node*> nodes_new;
    for(int i=0; i<nodes.size(); ++i)
    {
      std::string s = nodes[i]->name_;
      if(s != " ")
        s = "(" + s + ")";
      if(s.length() < maxlength)
        s += std::string(maxlength - s.length(), ' ');
      line.append(s);
      line.append(std::string(node_distance, ' '));
      if(nodes[i]->left_)
      {
        nodes_new.push_back(nodes[i]->left_);
        // next_line.append(std::string(next_line_ident, '-'));
      }
      else
      {
        nodes_new.push_back(new Node(" "));
        // next_line.append(maxlength + next_line_ident, ' ');
      }
      if(nodes[i]->right_)
      {
        nodes_new.push_back(nodes[i]->right_);
        // next_line.append(std::string(maxlength, ' '));
        // next_line.append(std::string(next_line_ident, '-'));
      }
      else
      {
        // next_line.append(maxlength + next_line_ident, ' ');
        nodes_new.push_back(new Node(" "));
      }
    }
    line += "\n";
    std::string next_line = std::string(line.length(), ' ');
    // for(int i=0; i<line.length(); i++)
    // {
    //   if(line[i] == '(')
    //   {
    //     next_line = next_line.replace(i - next_line_ident, next_line_ident, std::string(next_line_ident, '-'));
    //   }
    //   if(line[i] == ')')
    //   {
    //     next_line = next_line.replace(i, next_line_ident + i, std::string(next_line_ident, '-'));
    //   }
    // }
    next_line += "\n";
    result += line;
    result += next_line;
    nodes = nodes_new;
    // std::cout << "Ident: " << ident << std::endl;
    // std::cout << "Dist:  " << node_distance << std::endl;
    // std::cout << "************" << std::endl;
  }
  std::cout << result << std::endl;
  // print_preorder(&root, "");

  // std::cout << depth(&root) << std::endl;
  // Node root("a", new Node("b", nullptr, nullptr), nullptr);
  // std::cout << root.left_->name_ << std::endl;
}