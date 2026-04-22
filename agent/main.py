import json
import os

# ---------- Load JSON Tree Safely ----------
current_dir = os.path.dirname(__file__)
project_root = os.path.dirname(current_dir)

file_path = os.path.join(project_root, "tree", "reflection-tree.json")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert nodes into dictionary for fast lookup
nodes = {node["id"]: node for node in data["nodes"]}

# Start node
current = "START"
last_answer = None

print("\n🌳 Daily Reflection Tree Started\n")

# ---------- Tree Runner ----------
while True:
    node = nodes[current]

    node_type = node.get("type")
    text = node.get("text", "")

    print("\n" + "-" * 50)
    print(text)

    # ---------- QUESTION NODE ----------
    if node_type == "question":
        options = node.get("options", [])

        for i, opt in enumerate(options):
            print(f"{i + 1}. {opt}")

        choice = int(input("\nChoose option: ")) - 1
        last_answer = options[choice]

        # Move to next node (simple sequential logic)
        keys = list(nodes.keys())
        idx = keys.index(current)
        current = keys[idx + 1]

    # ---------- DECISION NODE ----------
    elif node_type == "decision":
        rules = node.get("rules", {})

        if last_answer in rules:
            current = rules[last_answer]
        else:
            current = list(rules.values())[0]

    # ---------- REFLECTION / BRIDGE / SUMMARY ----------
    elif node_type in ["reflection", "bridge", "summary"]:
        input("\nPress Enter to continue...")
        keys = list(nodes.keys())
        idx = keys.index(current)
        current = keys[idx + 1]

    # ---------- END ----------
    elif node_type == "end":
        print("\n✅ Session Completed. Good job reflecting today!")
        break

    else:
        keys = list(nodes.keys())
        idx = keys.index(current)
        current = keys[idx + 1]
