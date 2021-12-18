import statistics as stats
from collections import OrderedDict

sub_to_main = OrderedDict()

def getCriteria():
    """
    Accepts main and sub criteria nammes from the user
        and creates the corresponding matrix.
        
        Parameters:
        ------- 
            none

        Returns:
        -------
        `main criteria`: list of names of main criteria
        `sub criteria`: list of names of sub criteria
    """
    main_criteria = [main.strip() for main in (input("Enter main Criteria (comma-separated):\n").split(","))]
    sub_criteria_names = []
    criteria = OrderedDict()

    for main_criterion in main_criteria:
        sub_criteria = [sub.strip() for sub in (input(f"Enter sub-criteria of {main_criterion} (comma-separated):\n").split(","))]
        sub_criteria_names += sub_criteria
        for s in sub_criteria:
            sub_to_main[s] = main_criterion
        criteria[main_criterion] = sub_criteria
    return main_criteria, sub_criteria_names, criteria

def get_main_importance(criteria, experts):
    """
    Accepts expert weights of main criteria from the user
        and creates the corresponding matrix.
        
        Parameters:
        ------- 
           `criteria`: list of names of criteria
           `experts`: list of names of experts

        Returns:
        -------
        `importance list`: list of expert given weights of main criteria
     """
    importance_list = []
    for criterion in criteria:
        ratings = []
        for exp in experts:
            r = int(input(f"Enter importance rating for {criterion} by {exp}:\t"))
            ratings.append(r)
        sum_rating = sum(ratings)
        importance_list.append([criterion, sum_rating])
    
    return importance_list

def get_sub_importance(criteria_dict, experts):
    """
    Accepts expert weights of sub criteria from the user
        and creates the corresponding matrix.
        
        Parameters:
        ------- 
           `criteria`: list of names of criteria
           `experts`: list of names of experts
            
    imporatance_list = 
    [
        [                   ===> sub_importance_list
            [s1,r1]             ===> [sub_criteron, its_sum_of_ratings]
            [s2, r2]            ===> [sub_criteron, its_sum_of_ratings]
        ]
        [                   ===> sub_importance_list
            [s3, r3]            ===> [sub_criteron, its_sum_of_ratings]
            [s4, r4]            ===> [sub_criteron, its_sum_of_ratings]
        ]
    ]
    Returns:
        -------
        `importance list`: list of expert given weights of main and sub criteria
    """
    importance_list = []
    for main_criterion, sub_criteria in criteria_dict.items():
        print(f"Enter imporantace ratings for sub criteria of {main_criterion}\n")
        sub_importance_list = []
        for sub_criterion in sub_criteria:
            ratings = []
            for exp in experts:
                r = int(input(f"Enter importance rating for {sub_criterion}  by {exp}:\t"))
                ratings.append(r)
            sum_rating = sum(ratings)
            sub_importance_list.append([sub_criterion, sum_rating])
        importance_list.append(sub_importance_list)
    
    return importance_list

def sort(criteria):
    """
        Sorts the criteria in decending order.
        
        Parameters:
        ------- 
            `criteria`: list of names of criteria

        Returns:
        -------
            Sorted criteria.
    """
    return sorted(criteria, reverse=True, key=lambda x:x[1])

def sortByImportance(main_importance, sub_importance):
    """
        Sorts the main and sub importance list in decending order.
        
        Parameters:
        ------- 
           `main_importance`: unsorted main importance values.
           `sub_importance`: unsorted sub importance values.
 
        Returns:
        -------
            Sorted main and sub importance list.
    """
    sorted_main_importance = sort(main_importance)

    sorted_sub_importance = []
    for inner_sub_importance_list in sub_importance:
        sorted_sub_importance_list = sort(inner_sub_importance_list)
        sorted_sub_importance.append(sorted_sub_importance_list)

    return sorted_main_importance, sorted_sub_importance


def get_main_sj_values(sorted_main_criteria, experts):
    """
    Gets sj values of every main criterion and returns dictionary of 
        criterion, sj_value pairs

    Args:
        sorted_main_criteria (list of lists): [
            contains list of criteria names and corresponding importance ratings
            Eg:
                [
                    ["main criterion 1", 5],
                    ["main criterion 2", 7],
                    ["main criterion 3", 1],
                ]
            ]
        experts (list): [ list of names of experts]
    Returns:
        main_sj_dic (dict): [ 
            A dictionary of criterion name and corresponding sj value pairs
            ]
    """
    main_sj = OrderedDict()
    main_sj[sorted_main_criteria[0][0]] = 0

    for i in range(1, len(sorted_main_criteria)):
        sj_values = []
        criterion_rating_pair = sorted_main_criteria[i]
        criterion = criterion_rating_pair[0]
        for exp in experts:
            sj = float(input(f"Enter comparative significance (sj) value of {criterion} by {exp}\t"))
            sj_values.append(sj)
        
        mean_sj = stats.mean(sj_values)
        main_sj[criterion] = mean_sj
    
    return main_sj


def get_sub_sj_values(sorted_sub_criteria, experts):
    """
    Gets sj values of every sub criterion and returns dictionary of 
        criterion, sj_value pairs

    Args:
        sorted_sub_criteria (list of lists): [
            contains list of criteria names and corresponding importance ratings
            Eg:
                [
                    ["sub criterion 1", 5],
                    ["sub criterion 2", 7],
                    ["sub criterion 3", 1],
                ]
            ]
        experts (list): [ list of names of experts]
    Returns:
        sub_sj_dic (dict): [ 
            A dictionary of criterion name and corresponding sj value pairs
            ]
    """
    sub_sj = OrderedDict()

    for inner_sub_criteria in sorted_sub_criteria:
        sub_sj[inner_sub_criteria[0][0]] = 0
        main_criterion = sub_to_main.get(inner_sub_criteria[0][0])
        print(f"\nEnter comparative significance values for sub criteria of {main_criterion}")
        for i in range(1, len(inner_sub_criteria)):
            sj_values = []
            criterion_rating_pair = inner_sub_criteria[i]
            criterion = criterion_rating_pair[0]

            for exp in experts:
                sj = float(input(f"Enter comparative significance (sj) value of {criterion} by {exp}\t"))
                sj_values.append(sj)
            
            mean_sj = stats.mean(sj_values)
            sub_sj[criterion] = mean_sj
    
    return sub_sj

def get_inputs():
    """
    Accepts expert names from the user
        and creates the corresponding matrix.
        
        Parameters:
        ------- 
            `criteria`: list of names of criteria

        Returns:
        -------
        
     """
    experts = [name.strip() for name in (input("Enter name of the experts (comma-separated):\n").split(","))]
    main_criteria, sub_criteria_names, criteria = getCriteria()

    main_importance = get_main_importance(main_criteria, experts)
    sub_importance = get_sub_importance(criteria, experts)

    sorted_main_imp, sorted_sub_imp = sortByImportance(main_importance, sub_importance)

    main_sj = get_main_sj_values(sorted_main_imp, experts)
    sub_sj = get_sub_sj_values(sorted_sub_imp, experts)

    return criteria, main_importance, sub_importance, sorted_main_imp, sorted_sub_imp, main_sj, sub_sj

def calculate_kj_qj(sj_dict):
    """
       Calculates kj and qj values.
        
        Parameters:
        ------- 
            `sj_dict`: list of sj values.

        Returns:
        kj and qj list.
    """
    kj_dict = OrderedDict()
    qj_dict = OrderedDict()
    qj_prev = 1

    for criterion, sj in sj_dict.items():
        kj = sj + 1
        qj = qj_prev / kj
        qj_prev = qj

        kj_dict[criterion] = kj
        qj_dict[criterion] = qj

    return kj_dict, qj_dict


def calculate_weights(sj_dict):
    """
       Calculates wj values.
        
        Parameters:
        ------- 
            `sj_dict`: list of sj values.

        Returns:
        wj list.
    """
    kj_dict, qj_dict = calculate_kj_qj(sj_dict)
    
    wj_dict = OrderedDict()
    qj_sum = 0
    
    for qj in qj_dict.values():
        qj_sum += qj
    
    for criterion, qj in qj_dict.items():
        wj_dict[criterion] = qj / qj_sum
    
    return kj_dict, qj_dict, wj_dict


def calculate_global_weights(wj_main, wj_sub):
    """
       Calculates global weight values.
        
        Parameters:
        ------- 
            `wj_main`: list of main criteria wj values.
            `wj_sub`: list of sub criteria wj values.
        Returns:
        Global weight list.
     """
    global_weights = OrderedDict()
    for sub_criterion, wj_sub in wj_sub.items():
        global_weights[sub_criterion] = wj_main.get(sub_to_main.get(sub_criterion)) * wj_sub
    
    return global_weights

def sort_sub_criteria(global_weigths):
    """
       Calculates global weight values.
        
        Parameters:
        ------- 
            `global_weigths`: list of global weight values.
        Returns:
            'rank_dict' : Ranks of the sub criteria.
     """
    rank_dict = OrderedDict()

    global_weights_list = [[sub_criterion, wj_sub] for sub_criterion, wj_sub in global_weigths.items()]
    sorted_global_weights = sort(global_weights_list)

    for index, sub_rank in enumerate(sorted_global_weights):
        criterion = sub_rank[0]
        rank = index + 1
        rank_dict[criterion] = rank
    
    return rank_dict


def print_results(criteria_dict, wj_main, wj_sub, ranks):
    """
      Prints the sorted list with corresponding ranking
       
        Parameters:
        ------- 
        'criteria_dict' : Names of criteria.
        'wj_main': list of main criteria wj values.
        'wj_sub': list of sub criteria wj values.
        'rank_dict' : Ranks of the sub criteria.

        Returns:
        -------
        Sorted List of criteria names, relative & global weights and rank.
    """

    print("\nThe Ranking:\n")
    main_index = 1
    for main_criterion, sub_criteria in criteria_dict.items():
        print("\nSr. No.\t\tMain Criterion\tRelative Weight")
        main_rel_wt = wj_main.get(main_criterion)
        print(f"{main_index}\t\t{main_criterion}\t\t{main_rel_wt}\n" )
        
        print("  Sr. No.\tSub Criteria\tGlobal Weights\t\tRank")
        for sub_index, sub_criterion in enumerate(sub_criteria):
            rank = ranks.get(sub_criterion)
            global_wt = global_weights.get(sub_criterion)
            print("  " + chr(sub_index + 97) + ".\t\t" + sub_criterion, "\t\t" + str(global_wt) + "\t" + str(rank))
        
        main_index +=1
        print("\n"+ "-"*60)


if __name__ == "__main__":
    criteria_dict, main_importance, sub_importance, sorted_main_imp, sorted_sub_imp, main_sj, sub_sj = get_inputs()
    
    kj_main, qj_main, wj_main = calculate_weights(main_sj)
    kj_sub, qj_sub, wj_sub =  calculate_weights(sub_sj)

    # get global weigths
    global_weights = calculate_global_weights(wj_main, wj_sub)

    # sort on the basis of global weights
    ranks = sort_sub_criteria(global_weights)

    print_results(criteria_dict, wj_main, wj_sub, ranks)
