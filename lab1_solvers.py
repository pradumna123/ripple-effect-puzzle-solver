"""
PRADUMNA SURYAWANSHI
"""
import sys
import time
import datetime


class Solver:
    """
    a solver class that solves the maze using different methods.
    """
    __slots__ = ["maze", "first_element"]

    def __init__(self, maze):
        self.maze = maze

    def mrv_solver(self):
        """
        the best solver mrv+fc
        :return:
        """
        # self.maze.region_sizes()
        start = time.time()
        self.maze.fill_node_withlowstpossiblevalues(self.maze.get_firstelement(), 1)
        end = time.time()
        print(end - start)
        self.maze.create_dict_visitedList()
        node = self.maze.get_next_lowest_legal_values()
        if node == None:
            print("mrv+fc solver ")
            return
        else:
            self.maze.dict_visited[self.maze.global_dict_objs.get(node).string_main] = False
        self.maze.printmaze()
        start = time.time()
        print(self._mrv_solver(self.maze.global_dict_objs.get(self.maze.get_next_lowest_legal_values())))
        end = time.time()
        print("mrv - fc solver : ", end - start)

    def _mrv_solver(self, node):
        """
         A simple mrv+fc solver
        :param node:
        :return:
        """
        value = 0
        list_of_edited_nodes = list()
        # node to start filling values:
        # 1) get a dict of the current maze and check for a zero length possible value i.e a false from the function
        # 2) now get the possible values of the node form dict
        # 3)  select a value and generate a call mrv on the graph using value 2
        # 4) after that generate a dict again and see if you get a none in list of values if yes revert the changes.
        # 4) call the next smallest value  node method   and call the mrv solver again
        # print(self.maze.printmaze(), node, "1")
        dict_of_possible_values, status = self.maze.dict_with_possible_list()
        if status == False:
            # failed somewhere so we get possible_values for one node as none
            return False, 1
        list_of_possible_values = dict_of_possible_values[node.string_main]
        # if node.string_main == "2$5":
        #     list_of_possible_values = list_of_possible_values[::-1]
        for i in list_of_possible_values:
            # set a value for  the node
            node.value = int(i)
            # call the mrv to see if we can curtail the possible values
            stat1 = self.maze.fill_node_withlowstpossiblevalues(node, 2)
            # print("")
            # print("")
            # print(stat1)
            # print("1", node.string_main)
            # print(dict_of_possible_values)
            # print(self.maze.printmaze())
            # print("!!!!", stat1)
            stat12 = stat1[0]
            if stat12 == "N":
                stat12 = None
            list_of_edited_nodes = stat1[1]

            # print(self.maze.fill_node_withlowstpossiblevalues(self.maze.get_firstelement(), 2))
            # if stat1 == None:
            #     # somethng wrong reset and continue
            #     self.maze.reset_dict_with_possible_list(dict_of_possible_values, node, 1)
            #     continue

            dict_of_possible_values2, status = self.maze.dict_with_possible_list()
            # print(dict_of_possible_values2)
            if status == False:
                # failed somewhere so we get possible_values for one node as none
                self.maze.reset_dict_with_possible_list(dict_of_possible_values, node, 1)
                if len(list_of_edited_nodes) > 0:
                    while len(list_of_edited_nodes) > 0:
                        vv = list_of_edited_nodes.pop(0)
                        self.maze.global_dict_objs.get(vv).value = "."
                        self.maze.global_dict_objs.get(vv).realvalue2 = False
                    # print("2")
                    # self.maze.printmaze()
                    continue
            # self.maze.print_possbile_valuesize()
            next_node = self.maze.global_dict_objs.get(self.maze.get_next_lowest_legal_values())
            if next_node == None:
                # we have parsed the entire matrix
                return True, value + 1
            stat, value_temp = self._mrv_solver(next_node)
            value += value_temp
            if stat == True:
                return True, value + 1
            else:
                # when the status if false
                self.maze.reset_dict_with_possible_list(dict_of_possible_values, node, 1)
                if len(list_of_edited_nodes) > 0:
                    while len(list_of_edited_nodes) > 0:
                        vv = list_of_edited_nodes.pop(0)
                        self.maze.global_dict_objs.get(vv).value = "."
                        self.maze.global_dict_objs.get(vv).realvalue2 = False
                continue
        # print("3")
        # self.maze.printmaze()

        # we exhausted the values so rest the dict as something went wrong here and return false
        self.maze.reset_dict_with_possible_list(dict_of_possible_values, node, 2)
        if len(list_of_edited_nodes) > 0:
            while len(list_of_edited_nodes) > 0:
                vv = list_of_edited_nodes.pop(0)
                self.maze.global_dict_objs.get(vv).value = "."
                self.maze.global_dict_objs.get(vv).realvalue2 = False
        return False, value + 1

    def dfs_solver(self):
        """
        brute force solver
        :return:
        """
        self.first_element = self.maze.get_firstelement()
        start = time.time()
        print(self._solver(self.first_element))
        end = time.time()
        print("a simple brute force solver :", end - start)

    def dfs_solver1(self):
        """
        mrv solver
        :return:
        """
        # print("Start")
        # self.first_element = self.maze.get_firstelement()
        string = "6$7"
        # print(self.first_element, " \n", self.first_element.returnallattritubes())
        # print(self.maze.get_possible_values_for_a_node(self.maze.global_dict_objs.get(string)))
        # print(self.maze.get_neighbour(self.maze.global_dict_objs.get(string)))
        # print(self.maze.get_possible_values_for_a_node(self.maze.get_firstelement()))
        self.maze.create_dict_visitedList()
        start = time.time()
        print("start :: ", start)
        print(datetime.datetime.now())
        print(self._solver1(self.maze.global_dict_objs.get(self.maze.get_next_lowest_legal_values_2())))
        end = time.time()
        print("mrv solver::", end - start)

    def _solver(self, node):
        """brute force solver"""
        value = 0
        # possible_values= the reduced set,
        # possible_selections= set based on region size
        possible_values, possbile_slections = self.maze.get_possible_values_for_a_node(node)
        # print(self.maze.printmaze(), node, "1", possible_values)
        if possible_values == None:
            node.reset_values()
            # print(self.maze.printmaze(), node, "2", possible_values)
            return False, 1
        for i in possbile_slections:
            # set node values
            if i not in possible_values:
                continue
            node.value = str(i)
            # get neigbhours
            # 1) exit condition
            neigbh_node = self.maze.get_neighbour(node)
            # neigbh_node = self.maze.get_neighbour(node)
            # print(self.maze.printmaze(), node, "3")
            if neigbh_node != None:
                status, value_temp = self._solver(neigbh_node)
                value += value_temp
                # print(value)
                if status == True:
                    return True, value + 1
                else:
                    continue
            if neigbh_node == None:
                return True, value + 1
        node.reset_values()
        return False, value + 1

    def _solver1(self, node):
        """use mrv solver without fc"""
        value = 0
        # possible_values= the reduced set,
        # possible_selections= set based on region size
        dict_of_possible_values, status = self.maze.dict_with_possible_list()
        if status == False:
            # failed somewhere so we get possible_values for one node as none
            node.reset_values()
            if node.realvalue != True:
                node.list_of_possible_values = None
            self.maze.dict_visited[node.string_main] = False
            self.maze.reset_dict_with_possible_list(dict_of_possible_values, node, 2)
            return False, 1
        list_of_possible = node.list_of_possible_values
        possible_values, possbile_slections = self.maze.get_possible_values_for_a_node(node)
        if node.string_main == "2$5":
            possible_values = possible_values[::-1]
        # node.list_of_possible_values = possible_values
        # dict_of_possible_values, status = self.maze.dict_with_possible_list()
        # print(self.maze.printmaze(), node, "1", possible_values)
        # print(self.maze.printmaze(), node, "1", possible_values)
        # print(node.string_main)
        if possible_values == None:
            node.reset_values()
            if node.realvalue != True:
                node.list_of_possible_values = None
            self.maze.dict_visited[node.string_main] = False
            self.maze.reset_dict_with_possible_list(dict_of_possible_values, node, 2)
            # print(self.maze.printmaze(), node, "2", possible_values)
            return False, 1
        for i in possible_values:

            # set node values
            node.value = str(i)
            self.maze.update_dict(node)
            # print(self.maze.printmaze(), node, "2", possible_values)
            # get neigbhours
            # 1) exit condition
            dict_of_possible_values2, status = self.maze.dict_with_possible_list()
            if status == False:
                self.maze.reset_dict_with_possible_list(dict_of_possible_values, node, 1)
                node.reset_values()
                node.list_of_possible_values = list_of_possible
                continue
            neigbh_node = self.maze.global_dict_objs.get(self.maze.get_next_lowest_legal_values_2())
            # neigbh_node = self.maze.get_neighbour(node)
            # print(self.maze.printmaze(), node, "3")
            if neigbh_node != None:
                status, value_temp = self._solver1(neigbh_node)
                value += value_temp
                # print(value)
                if status == True:
                    # last iteration was true i.e right
                    return True, value + 1
                else:
                    self.maze.reset_dict_with_possible_list(dict_of_possible_values, node, 1)

                    continue
            if neigbh_node == None:
                # we parsed the entire maze
                return True, value + 1
        node.reset_values()
        if node.realvalue != True:
            node.list_of_possible_values = list_of_possible
        self.maze.reset_dict_with_possible_list(dict_of_possible_values, node, 2)
        return False, value + 1


class RippleEffect:
    """
    a global representation of the maze
    """
    __slots__ = ["regions_in_puzzle", "x_size", "y_size", "global_dict_objs", "intial_Number",
                 "dict_smallest_possiblevalues", "dict_visited", "highest_region_size"]

    def __init__(self, lista, x_size, y_size):
        self.regions_in_puzzle = []
        self.x_size = x_size
        self.y_size = y_size
        self.global_dict_objs = {}
        self.intial_Number = lista
        self.highest_region_size = 0
        self.dict_visited = {}

    def update_dict(self, node):
        """
        helper function to update the dictionary
        :param node:
        :return:
        """
        # node_region = node.regions_id
        for i in self.regions_in_puzzle:
            for j in i.elements:
                if j.realvalue != True and self.dict_visited[j.string_main] != True:
                    a, b = self.get_possible_values_for_a_node(j)
                    j.list_of_possible_values = a

    def reset_dict_with_possible_list(self, dict, node, val):
        """
        resets the value of dict with values passed to it
        :param dict:
        :param node:
        :param val:
        :return:
        """
        for i in self.regions_in_puzzle:
            for j in i.elements:
                if self.dict_visited.get(j.string_main) != True:
                    listofalues = dict[j.string_main]
                    j.list_of_possible_values = listofalues
        if node != None:
            if val == 2 and node.realvalue != True:
                node.value = "."
            if val == 2:
                self.dict_visited[node.string_main] = False

    def dict_with_possible_list(self):
        # A function that returns dict whos value if the list of possible values for the node in that instance of revursion
        status = True
        possible_v_dict = {}
        for i in self.regions_in_puzzle:
            for j in i.elements:
                if j.list_of_possible_values == None or len(j.list_of_possible_values) == 0:
                    status = False
                possible_v_dict[j.string_main] = j.list_of_possible_values
        return possible_v_dict, status

    def dict_with_possible_list2(self):
        # A function that returns dict whos value if the list of possible values for the node in that instance of revursion
        status = True
        possible_v_dict = {}
        for i in self.regions_in_puzzle:
            for j in i.elements:
                if j.list_of_possible_values == None or len(j.list_of_possible_values) == 0:
                    status = False
                possible_values, possbile_slections = self.get_possible_values_for_a_node(j)
                j.list_of_possible_values = possible_values
                possible_v_dict[j.string_main] = j.list_of_possible_values
        return possible_v_dict, status

    def add_regions(self, region):
        self.regions_in_puzzle.append(region)

    def create_dict_visitedList(self):
        """
        creates a dictionary
        :return:
        """
        # the dict will have key as the node and value as the boolean values as t/f
        # t --> when the node has a right element
        # f--> when the node does not have a right value
        for i in self.regions_in_puzzle:
            for j in i.elements:
                if j.realvalue != True:
                    self.dict_visited[j.string_main] = False
                else:
                    self.dict_visited[j.string_main] = True
        return self.dict_visited

    def get_next_lowest_legal_values(self):
        """
        a hlper function for getting the lowest legal value node from the grpah
        :return:
        """
        val = self.highest_region_size
        obj = None
        for o in range(val + 1):
            for i in self.regions_in_puzzle:
                for j in i.elements:
                    if self.dict_visited[j.string_main] != True and len(
                            j.list_of_possible_values) == o:
                        val = len(j.list_of_possible_values)
                        obj = j
                        self.dict_visited[obj.string_main] = True
                        return obj.string_main
        if obj == None:
            return None

    def get_next_lowest_legal_values_2(self):
        """
        a helper function
        :return:
        """
        val = self.highest_region_size
        obj = None
        for o in range(val + 1):
            for i in self.regions_in_puzzle:
                for j in i.elements:

                    if self.dict_visited[j.string_main] != True and len(
                            j.list_of_possible_values) == o and j.realvalue != True:
                        val = len(j.list_of_possible_values)
                        obj = j
                        self.dict_visited[obj.string_main] = True
                        return obj.string_main
        if obj == None:
            return None

    def set_neig(self):
        """
        allocate neighbours to all nodes

        :return:
        """
        for i in self.regions_in_puzzle:
            for j in i.elements:
                # "left_node", "right_node", "top_node", "down_node"
                j.left_node = self.get_horilefttelement(j.string_main)
                j.right_node = self.get_horirightelement(j.string_main)
                j.top_node = self.get_verticaltopelement(j.string_main)
                j.down_node = self.get_verticaldownelement(j.string_main)

    def region_sizes(self):
        """
        prints the region sizes helper function
        :return:
        """
        for i in self.regions_in_puzzle:
            print(str(i.size) + " ** " + str(i.id))

    def __str__(self):
        str1 = "" + "\n"
        for i in self.regions_in_puzzle:
            str1 += str(i) + " $$$" + "\n"
        return str1

    def calulate_size_of_regions(self):
        """
        calculates the size of region
        :return:
        """
        for i in self.regions_in_puzzle:
            i.allocatesize()
            if i.size > self.highest_region_size:
                self.highest_region_size = i.size

    def fill_node_withlowstpossiblevalues(self, start, val):
        """
        fills the node with lowest possible values
        :param start:
        :param val:
        :return:
        """
        list_of_edited_nodes = []
        # scroll through all nodes and find its possible values if we find a node to be 1 then we fill it right there and this goes on.
        # call the recursive method.
        c = 0
        # self.print_possbile_valuesize()
        counter, b = self._fill_node_withlowstpossiblevaluesr(start, val)
        if len(b) > 0:
            for item in b:
                list_of_edited_nodes.append(item)

        # print("@@@", counter, list_of_edited_nodes)

        if counter == None or counter == 0:
            lista = ["N", list_of_edited_nodes]
            return lista
        c = counter
        while counter > 0:
            counter, b = self._fill_node_withlowstpossiblevaluesr(start, val)
            c = counter
            if len(b) > 0:
                for item in b:
                    list_of_edited_nodes.append(item)
            # print("$$", counter, b)
            if counter == None or counter == 0:
                lista = ["N", list_of_edited_nodes]
                return lista
        # self.print_possbile_valuesize()

    def _fill_node_withlowstpossiblevaluesr(self, node, val):

        """
        fills the node with 1 possible value
        :param node:
        :param val:
        :return:
        """

        list_of_edited_nodes = []
        countr = 0
        for i in self.regions_in_puzzle:
            for j in i.elements:
                if val == 1 or val == 2 and self.dict_visited[
                    j.string_main] != True and j.realvalue != True and j.realvalue2 != True:
                    possible_values, possbile_slections = self.get_possible_values_for_a_node(j)
                    if possible_values == None:
                        j.list_of_possible_values = possible_values
                        return None, list_of_edited_nodes
                    if j.realvalue != True and len(possible_values) == 1:
                        list_of_edited_nodes.append(j.string_main)
                        j.value = possible_values[0]
                        if val == 1:
                            j.realvalue = True
                        else:
                            j.realvalue2 = True
                            j.list_of_possible_values = possible_values
                        countr += 1
                    else:
                        j.list_of_possible_values = possible_values

        return countr, list_of_edited_nodes

    # set start node

    def print_possbile_valuesize(self):
        """
        helper function used for debugging
        :return:
        """
        ccounter = 0
        for i in self.regions_in_puzzle:
            for j in i.elements:
                if j.realvalue == False:
                    ccounter += 1
                    string = j.string_main + " **** size of poss " + str(
                        len(j.list_of_possible_values)) + " r_id " + str(j.regions_id) + \
                             " %%%r_size " + str(self.regions_in_puzzle[j.regions_id].size)
                    print(string)
        print("**************", ccounter)

    def calculate_no_ofBlocks(self):
        """
        calculates the number of blocks in graph , a helper function to see if graph is created correctly
        :return:
        """
        no_of_blocks = 0
        for i in self.regions_in_puzzle:
            no_of_blocks += i.size
        return no_of_blocks

    def get_possible_values_for_a_node(self, node):
        """
        returns none if no possible values
        else
        returns a list of possible values
        :param node:
        :return:
        """
        list_values = []
        # if the node has a predefined value
        if node.realvalue == True:
            list_values.append(int(node.value))
            return list_values, list_values
        else:
            # if the node does not have  a predefined value
            # call getvalues from region for a partiuclar node
            node_region_id = node.regions_id
            set1 = []
            set12 = self.regions_in_puzzle[node_region_id].get_possbilevalues(node)
            if set12 != None:
                possible = set12.copy()
            # remove redundant values
            if set12 == None:
                return None, None
            set12 = self.get_neighbouring_element_for_reduced_set(node, self.regions_in_puzzle[node_region_id], set12)
            if len(set12) == 0:
                # i.e no possible values have been found
                return None, None
            else:
                # we have some possible values for the node
                return set12, possible

    def get_neighbouring_element_for_reduced_set(self, node, node_region, set123):
        """
        this will call k horizontal elements in right and left direction of the node ..where k is the size of the region
        used for reducing the redundancy in the possible values for a node
        :param node:
        :param node_region:
        :return:
        """
        stringtemp = node.string_main
        region_size = node_region.size
        left_node = stringtemp
        right_node = stringtemp
        top_node = stringtemp
        down_node = stringtemp

        for i in range(region_size):
            if left_node != None:
                left_node = self.global_dict_objs.get(left_node).left_node
                if left_node != None and self.global_dict_objs.get(left_node).value != "." and int(
                        self.global_dict_objs.get(left_node).value) in set123 and int(
                    self.global_dict_objs.get(left_node).value) >= (i + 1):
                    set123.remove(int(self.global_dict_objs.get(left_node).value))
            if right_node != None:
                right_node = self.global_dict_objs.get(right_node).right_node
                if right_node != None and self.global_dict_objs.get(right_node).value != "." and int(
                        self.global_dict_objs.get(right_node).value) in set123 and int(
                    self.global_dict_objs.get(right_node).value) >= (i + 1):
                    set123.remove(int(self.global_dict_objs.get(right_node).value))
            if top_node != None:
                top_node = self.global_dict_objs.get(top_node).top_node
                if top_node != None and self.global_dict_objs.get(top_node).value != "." and int(
                        self.global_dict_objs.get(top_node).value) in set123 and int(
                    self.global_dict_objs.get(top_node).value) >= (i + 1):
                    set123.remove(int(self.global_dict_objs.get(top_node).value))
            if down_node != None:
                down_node = self.global_dict_objs.get(down_node).down_node
                if down_node != None and self.global_dict_objs.get(down_node).value != "." and int(
                        self.global_dict_objs.get(down_node).value) in set123 and int(
                    self.global_dict_objs.get(down_node).value) >= (i + 1):
                    set123.remove(int(self.global_dict_objs.get(down_node).value))
        return set123

    def get_horirightelement(self, string):
        """
        gives the horizontal right element
        :param string:
        :return:
        """
        stringtemp = string
        i_i = int(stringtemp[:stringtemp.index('$')])
        j_j = int(stringtemp[stringtemp.index('$') + 1:])
        var_name = str(i_i) + "$" + str(j_j + 1)
        while True:
            if int(var_name[var_name.index('$') + 1:]) <= len(
                    self.intial_Number[i_i]) - 1 and var_name in self.global_dict_objs:
                return self.global_dict_objs[var_name].string_main
            else:
                if int(var_name[var_name.index('$') + 1:]) <= len(self.intial_Number[i_i]) - 1:
                    j_j += 1
                    var_name = str(i_i) + "$" + str(j_j + 1)
                else:
                    return None

    def get_horilefttelement(self, string):
        """
        returns the horizontal left element
        :param string:
        :return:
        """
        stringtemp = string
        i_i = int(stringtemp[:stringtemp.index('$')])
        j_j = int(stringtemp[stringtemp.index('$') + 1:])
        var_name = str(i_i) + "$" + str(j_j - 1)
        while True:
            if int(var_name[var_name.index('$') + 1:]) - 1 >= 0 and var_name in self.global_dict_objs:
                return self.global_dict_objs[var_name].string_main
            else:
                if int(var_name[var_name.index('$') + 1:]) - 1 >= 0:
                    j_j -= 1
                    var_name = str(i_i) + "$" + str(j_j - 1)
                else:
                    return None

    def get_verticaltopelement(self, string):
        """
        returns the vertical top element
        :param string:
        :return:
        """
        stringtemp = string
        i_i = int(stringtemp[:stringtemp.index('$')])
        j_j = int(stringtemp[stringtemp.index('$') + 1:])
        var_name = str(i_i - 1) + "$" + str(j_j)
        while True:
            if int(var_name[:var_name.index('$')]) - 1 >= 0 and var_name in self.global_dict_objs:
                return self.global_dict_objs[var_name].string_main
            else:
                if int(var_name[:var_name.index('$')]) - 1 >= 0:
                    i_i -= 1
                    var_name = str(i_i - 1) + "$" + str(j_j)
                else:
                    # no top element from present node
                    return None

    def get_verticaldownelement(self, string):
        """
        returns the vertical down element
        :param string:
        :return:
        """
        stringtemp = string
        i_i = int(stringtemp[:stringtemp.index('$')]) + 1
        j_j = int(stringtemp[stringtemp.index('$') + 1:])
        var_name = str(i_i) + "$" + str(j_j)
        while True:
            if int(var_name[:var_name.index('$')]) + 1 <= len(
                    self.intial_Number) - 1 and self.global_dict_objs.get(var_name) != None:
                return self.global_dict_objs.get(var_name).string_main
            else:
                if int(var_name[:var_name.index('$')]) + 1 <= len(self.intial_Number) - 1:
                    i_i += 1
                    var_name = str(i_i) + "$" + str(j_j)
                else:
                    # no next element at down
                    return None

    def get_firstelement(self):
        """returns the first element"""
        if self.regions_in_puzzle[0] != None:
            return self.regions_in_puzzle[0].elements[0]

    def create_a_global_dict(self):
        """
        a global dict is created  to help in make tasks where duplicates are to be avoided and instant to nodes from other regions
        :return:
        """
        for i in self.regions_in_puzzle:
            for j in i.elements:
                self.global_dict_objs[j.string_main] = j
                j.regions_id = i.id
        self.insert_dict()
        self.give_incr_id()

    def insert_dict(self):
        """
        a global dict has been created which is then inserted in every region to make it aware of every other region
        :return:
        """
        for i in self.regions_in_puzzle:
            for j in i.elements:
                j.global_dict_copy = self.global_dict_objs

    def give_incr_id(self):
        """
        gives the id to region after the graph has been created
        :return:
        """
        for i in range(len(self.regions_in_puzzle)):
            for j in range(len(self.regions_in_puzzle[i].elements)):
                self.regions_in_puzzle[i].elements[j].id = j

    def get_neighbour(self, node):
        """
        gets the next node to process
        :param node:
        :return:
        """
        # define neighbour on 2 ways 1) items in same region and 2)after that items in next region starting from 0.
        region_id = node.regions_id
        node_id = node.id
        # get region size
        region_size = self.regions_in_puzzle[region_id].size
        if region_id <= len(self.regions_in_puzzle) - 1:
            if node_id < region_size - 1:
                # i.e more nodes in the region
                return self.regions_in_puzzle[region_id].elements[node_id + 1]
            else:
                if region_id + 1 <= len(self.regions_in_puzzle) - 1:
                    return self.regions_in_puzzle[region_id + 1].elements[0]
                else:
                    return None

    # will read the file and manintain the list data structure
    # will call both the

    def printmaze(self):
        """
        prints the maze
        :return:
        """
        f_e = self.get_firstelement()
        list_maze = []
        top_down = f_e.string_main
        r_e = f_e.string_main
        hori_element = []

        for j in range(self.x_size):
            for i in range(self.y_size):
                if self.global_dict_objs.get(r_e) != None:
                    hori_element.append(str(self.global_dict_objs.get(r_e).value))
                    # hori_element.append(str(self.global_dict_objs.get(r_e).value) + str(":") + str(
                    #     self.global_dict_objs.get(r_e).string_main))
                else:
                    continue
                # string1 = str(self.global_dict_objs.get(r_e).value) + str(":") + str(
                #     self.global_dict_objs.get(r_e).string_main)
                # alpha = ''
                # if self.global_dict_objs.get(r_e).list_of_possible_values != None and self.global_dict_objs.get(
                #         r_e).list_of_possible_values != []:
                #     for item in self.global_dict_objs.get(r_e).list_of_possible_values:
                #         alpha += str(item)
                # alpha = " lis_of_values :: " + alpha
                # string1 += alpha
                # hori_element.append(string1)

                r_e = self.get_horirightelement(r_e)
            if self.global_dict_objs.get(top_down) != None:
                list_maze.append(hori_element)
                hori_element = []
                top_down = self.get_verticaldownelement(self.global_dict_objs.get(top_down).string_main)
                if self.global_dict_objs.get(top_down) != None:
                    r_e = self.global_dict_objs.get(top_down).string_main
        string_maze = ""

        for i in list_maze:
            for j in i:
                string_maze += str(j)
            string_maze += '\n'

        return string_maze


class Regions:
    """
    a region level representation of the region of graph
    """
    __slots__ = ["elements", "size", "possible_mutations_for_this_region", "id"]

    def __init__(self, id, size):
        self.size = size
        self.elements = []
        self.id = id
        # this will store all mutated versions of this region. in form of a region object
        self.possible_mutations_for_this_region = []

    def add_element(self, element):
        """
        a helper function useful while creating the graph
        :param element:
        :return:
        """
        self.elements.append(element)

    def all_possible_values(self):
        """
        a general function to get all possible values for the node
        :return:
        """
        values = []
        for i in self.elements:
            values.append(i.valueof)
        items_not_used = []
        for i in range(1, self.size + 1):
            if i not in values:
                items_not_used.append(i)
        return items_not_used

    def get_possbilevalues(self, node):
        """
        gets the possible value for a node from the region.
        :param node:
        :return:
        """
        possbile_list = self.possible_mutations_for_this_region.copy()
        for j in self.elements:
            if j.value != "." and int(j.value) in possbile_list:
                possbile_list.remove(int(j.value))
        if len(possbile_list) > 0:
            return possbile_list
        else:
            return None

    # 1) test if the node belongs to this region
    # 2) get all possible values for the region
    # 3) scroll through each element and if the element has a value remove that element from list at step 2

    def allocatesize(self):
        """allocates the size of the region well does many more things"""
        self.size = len(self.elements)
        for i in range(0, self.size):
            self.possible_mutations_for_this_region.append(i + 1)
        # assigns value 1 if the region size is 1 .... --> i.e the region only contains only 1 square so we assign the value 1 to the
        if self.size == 1:
            if self.elements[0].value == ".":
                self.elements[0].value = 1
                self.elements[0].realvalue = True

        for i in self.elements:
            i.list_of_possible_values = self.possible_mutations_for_this_region

    def __str__(self):
        l = "" + str(self.id) + '.' + " "
        for i in self.elements:
            l += str(i) + " "
        return l


class ElementAlpha:
    """
    a element class the most basic entity
    """
    __slots__ = ["string_main", "i", "j", "regions_id", "listofpossible", "value", "realvalue", "global_dict_copy",
                 "id", "left_node", "right_node", "top_node", "down_node", "list_of_possible_values", "realvalue2"]

    def __init__(self, string_main, region_id=None, value=None):
        self.string_main = string_main
        # self.i = 0
        self.list_of_possible_values = []
        self.realvalue2 = False
        self.id = None
        if value == ".":
            self.realvalue = False
        else:
            self.realvalue = True
        self.regions_id = region_id
        self.value = value
        self.global_dict_copy = {}

    def __str__(self):
        """
        stinng representation of the node
        :return:
        """
        return self.string_main

    def returnallattritubes(self):
        """
        a detailed description of the node
        :return:
        """
        arrtributes = ""
        arrtributes += 'string main :' + str(self.string_main) + "\n"
        arrtributes += "region id :" + str(self.regions_id) + "\n"
        arrtributes += " id:" + str(self.id) + "\n" + "value:" + str(self.value)
        return arrtributes

    def reset_values(self):
        """
        resets the value of the node
        :return:
        """
        if self.realvalue != True:
            self.value = '.'
        else:
            return


def working_with_file(filename):
    """
    creates a list of list representation from the text file
    :param filename:
    :return:
    """
    """
    processes the file and returns a list of lists representation of the maze
    :param filename:
    :return:
    """
    file = open(filename, "r")
    list_of_numbers = []
    for line in file:
        line = line.strip('\n')
        list_1 = []
        for i in line:
            # if not (i ==" "):
            list_1.append(i)
        list_of_numbers.append(list_1)
    size_x, size_y = get_size(list_of_numbers[0])
    size_element2 = len(list_of_numbers[2])
    for i in list_of_numbers:
        if len(i) < size_element2:
            for j in range(len(i), size_element2 + 1):
                i.append(' ')
    return list_of_numbers


def get_n(listofnumbers, i, j, global_dict):
    """
    helper to create a region generates a region from the list
    :param listofnumbers:
    :param i:
    :param j:
    :param global_dict:
    :return:
    """
    list_ofelements = []
    global_dict[str(i) + "$" + str(j)] = True
    final = []
    queue = []
    # print("**", listofnumbers[i][j])
    tempi, tempj = i, j
    if tempi < len(listofnumbers) - 1 and tempj + 1 < len(listofnumbers[i]) - 1 and listofnumbers[tempi][
        tempj + 1] != "|" and listofnumbers[tempi][tempj + 1] != "-" and str(tempi) + "$" + str(
        tempj + 1) not in global_dict:
        # create a node of the next element
        node = ElementAlpha(str(i) + "$" + str(j + 1), value=listofnumbers[tempi][tempj + 1])
        global_dict[str(tempi) + "$" + str(tempj + 1)] = True
        # print(globsl_dict)
        # print(node.string_main)
        queue.append(node)
        list_ofelements.append(node)

    while len(queue) > 0:
        a = queue.pop(0)
        if a.value != " " and a.value != '-' and a.value != "|":
            stringtemp = a.string_main
            i_i = int(stringtemp[:stringtemp.index('$')])
            j_j = int(stringtemp[stringtemp.index('$') + 1:])
            # fill the queue

            # top

            if i_i - 1 < len(listofnumbers) and j_j < len(listofnumbers[i_i - 1]) and listofnumbers[i_i - 1][
                j_j] != "-" and listofnumbers[i_i - 1][j_j] != "|":
                if i_i - 1 < len(listofnumbers) and j_j < len(listofnumbers[i_i - 1]) and listofnumbers[i_i - 1][
                    j_j] == " ":
                    i_i -= 1
                if i_i - 1 < len(listofnumbers) and j_j < len(listofnumbers[i_i - 1]) and listofnumbers[i_i - 1][
                    j_j] != " ":
                    if str(i_i - 1) + "$" + str(j_j) not in global_dict:
                        node = ElementAlpha(str(i_i - 1) + "$" + str(j_j), value=listofnumbers[i_i - 1][j_j])
                        queue.append(node)
                        list_ofelements.append(node)
                        global_dict[node.string_main] = True
                if i_i + 1 < len(listofnumbers) and j_j < len(listofnumbers[i_i + 1]) and listofnumbers[i_i][
                    j_j] == " ":
                    i_i += 1

            # down

            if i_i + 1 < len(listofnumbers) and j_j < len(listofnumbers[i_i + 1]) and listofnumbers[i_i + 1][
                j_j] != "-" and listofnumbers[i_i + 1][j_j] != "|":
                if i_i + 1 < len(listofnumbers) and j_j < len(listofnumbers[i_i + 1]) and listofnumbers[i_i + 1][
                    j_j] == " ":
                    i_i += 1
                if i_i + 1 < len(listofnumbers) and j_j < len(listofnumbers[i_i + 1]) and listofnumbers[i_i + 1][
                    j_j] != " ":
                    if str(i_i + 1) + "$" + str(j_j) not in global_dict:
                        node = ElementAlpha(str(i_i + 1) + "$" + str(j_j), value=listofnumbers[i_i + 1][j_j])
                        queue.append(node)
                        list_ofelements.append(node)
                        global_dict[node.string_main] = True
                if i_i < len(listofnumbers) and j_j < len(listofnumbers[i_i + 1]) and listofnumbers[i_i][
                    j_j] == " ":
                    i_i -= 1

            # right
            if i_i < len(listofnumbers) and j_j + 1 < len(listofnumbers[i_i]) and listofnumbers[i_i][j_j + 1] != '|' and \
                    listofnumbers[i_i][j_j + 1] != '-':
                if i_i < len(listofnumbers) and j_j + 1 < len(listofnumbers[i_i]) and listofnumbers[i_i][
                    j_j + 1] == " ":
                    j_j += 1
                if i_i < len(listofnumbers) and j_j + 1 < len(listofnumbers[i_i]) and listofnumbers[i_i][
                    j_j + 1] != " ":
                    if str(i_i) + "$" + str(j_j + 1) not in global_dict:
                        node = ElementAlpha(str(i_i) + "$" + str(j_j + 1), value=listofnumbers[i_i][j_j + 1])
                        queue.append(node)
                        list_ofelements.append(node)
                        global_dict[node.string_main] = True
                if i_i < len(listofnumbers) and j_j < len(listofnumbers[i_i]) and listofnumbers[i_i][
                    j_j] == " ":
                    j_j -= 1

            # left
            if i_i < len(listofnumbers) and j_j - 1 < len(listofnumbers[i_i]) and listofnumbers[i_i][j_j - 1] != '|' and \
                    listofnumbers[i_i][j_j - 1] != '-':
                if i_i < len(listofnumbers) and j_j - 1 < len(listofnumbers[i_i]) and listofnumbers[i_i][
                    j_j - 1] == " ":
                    j_j -= 1
                if i_i < len(listofnumbers) and j_j - 1 < len(listofnumbers[i_i]) and listofnumbers[i_i][
                    j_j - 1] != " ":
                    if str(i_i) + "$" + str(j_j - 1) not in global_dict:
                        node = ElementAlpha(str(i_i) + "$" + str(j_j - 1), value=listofnumbers[i_i][j_j - 1])
                        queue.append(node)
                        list_ofelements.append(node)
                        global_dict[node.string_main] = True
                if listofnumbers[i_i][j_j] != '|':
                    if i_i < len(listofnumbers) and j_j + 1 < len(listofnumbers[i_i]) and listofnumbers[i_i][
                        j_j] == " ":
                        j_j += 1
    # for i in list_ofelements:
    #     print(i)
    if len(list_ofelements) > 0:
        return list_ofelements, True
    else:
        return list_ofelements, False


def create_region(listofnumbers, i, j, size_x, size_y, global_dct, region_counter):
    """
    helper to creating a grpah , creates a region
    :param listofnumbers:
    :param i:
    :param j:
    :param size_x:
    :param size_y:
    :param global_dct:
    :param region_counter:
    :return:
    """
    list_elements_h = []
    # print(len(listofnumbers[i]))
    # call get_n to get neighburs
    list_of_elements_in_region, status = get_n(listofnumbers, i, j, global_dct)
    if status == True:
        region = Regions(region_counter, len(list_of_elements_in_region) - 1)
        for i in list_of_elements_in_region:
            region.add_element(i)
        # print("regions created", region)
        return region, status
    else:
        return None, False


def process_the_list(listofnumbers, size_x, size_y):
    """
    helper to process the list and create a graph
    :param listofnumbers:
    :param size_x:
    :param size_y:
    :return:
    """
    # print(listofnumbers)
    graph_obj = RippleEffect(listofnumbers, size_x, size_y)
    global_dict = {}
    region_counter = 0
    for i in range(2, len(listofnumbers), 2):
        for j in range(0, len(listofnumbers[i])):
            # print(listofnumbers[i][j])
            if str(i) + str(j) not in global_dict:
                if listofnumbers[i][j] == '|':
                    # print(listofnumbers[i][j], i, j)
                    creted_region, status = create_region(listofnumbers, i, j, size_x, size_y, global_dict,
                                                          region_counter)
                    if status == True:
                        graph_obj.add_regions(creted_region)
                        region_counter += 1
    print("****************", graph_obj)
    graph_obj.calulate_size_of_regions()
    # print(graph_obj.calculate_no_ofBlocks())
    graph_obj.create_a_global_dict()
    graph_obj.set_neig()
    return graph_obj


def get_size(listofnumbers):
    string_procesosr = ''.join(listofnumbers)
    string_procesosr = string_procesosr.split(" ")
    size_x = int(string_procesosr[0])
    size_y = int(string_procesosr[1])
    return size_x, size_y


def process_1_file(filename):
    """
    helper to call brute force
    :param filename:
    :return:
    """
    globsl_dict = {}
    listofnumber = working_with_file(filename)
    size_x, size_y = get_size(listofnumber[0])
    graph_obj = process_the_list(listofnumber, size_x, size_y)
    solverobj_1 = Solver(graph_obj)
    # print(graph_obj.get_horirightelement("2$3"))
    solverobj_1.dfs_solver()
    print("", graph_obj.printmaze())


def process_2_file(filename):
    """
    helper to mrv
    :param filename:
    :return:
    """
    globsl_dict = {}
    listofnumber = working_with_file(filename)
    size_x, size_y = get_size(listofnumber[0])
    graph_obj = process_the_list(listofnumber, size_x, size_y)
    solverobj_1 = Solver(graph_obj)
    # print(graph_obj.get_horirightelement("2$3"))
    solverobj_1.dfs_solver1()
    print("", graph_obj.printmaze())


def process_3_file(filename):
    """
    helper to call mrv+fc
    :param filename:
    :return:
    """
    globsl_dict = {}
    listofnumber = working_with_file(filename)
    size_x, size_y = get_size(listofnumber[0])
    graph_obj = process_the_list(listofnumber, size_x, size_y)
    solverobj_1 = Solver(graph_obj)
    # print(graph_obj.get_horirightelement("2$3"))
    solverobj_1.mrv_solver()
    # solverobj_1.dfs_solver()
    # print(graph_obj.get_possible_values_for_a_node('2$1'))
    # print(graph_obj.printmaze())
    print("", graph_obj.printmaze())


def main():
    """
    THE CODE STARTS HERE
    :return:
    """
    if (len(sys.argv) != 2):
        print("************invalid input:::: pass the file name as argument to the code********")
    filename = sys.argv[1]

    process_1_file(filename)
    print("****" * 80)
    process_2_file(filename)
    print("****" * 80)
    process_3_file(filename)


main()
