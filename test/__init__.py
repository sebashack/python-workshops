import unittest
import sys
import os

src_path = str(os.path.join(os.getcwd(), "src"))
sys.path.insert(0, src_path)

if __name__ == "__main__":
    unittest.main()
