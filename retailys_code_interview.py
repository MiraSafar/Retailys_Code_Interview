import sys
from xml.etree.ElementTree import iterparse
from time import perf_counter

xml_file_path = "export_full.xml"


def timer(fn):

    def inner(*args, **kwargs):
        start_time = perf_counter()
        to_execute = fn(*args, **kwargs)
        end_time = perf_counter()
        execution_time = end_time - start_time
        print("-"*30)
        print('{0} took {1:.8f}s to execute'.format(fn.__name__, execution_time))
        print("-" * 30)
        return to_execute

    return inner


@timer
def get_total_num_products(file):

    print("Processing...")

    depth = 0
    product_count = 0

    for event, node in iterparse(file, events=['end', 'start']):
        if event == 'start':
            depth += 1

            if depth == 3 and node.tag == 'item':
                product_count += 1

        else:
            depth -= 1
            if node.tag == 'items':
                return product_count

        node.clear()


@timer
def list_all_products(file):
    depth = 0

    for event, node in iterparse(file, events=['end', 'start']):
        if event == 'start':
            depth += 1

            if depth == 3 and node.tag == 'item':
                print(node.attrib['name'])

        else:
            depth -= 1
            if node.tag == 'items':
                break

        node.clear()


@timer
def list_all_spare_parts(file):
    depth = 0
    spare_parts_node = False
    current_item = None

    for event, node in iterparse(file, events=['end', 'start']):
        if event == 'start':
            depth += 1

            if depth == 3 and node.tag == 'item':
                current_item = node.attrib['name']

            if node.tag == 'part' and node.attrib['categoryId'] == "1":
                spare_parts_node = True
                print("-"*30)
                print(current_item)

            if spare_parts_node and node.tag == 'item':
                print(f"----> Spare part: {node.attrib['name']}")

        else:
            depth -= 1
            if node.tag == 'items':
                break

            if node.tag == 'part':
                spare_parts_node = False

        node.clear()


if __name__ == '__main__':
    if sys.argv[1] == "1":
        print(f"Total number of products: {get_total_num_products(xml_file_path)}")
    elif sys.argv[1] == "2":
        list_all_products(xml_file_path)
    elif sys.argv[1] == "3":
        list_all_spare_parts(xml_file_path)

