import statistics as stats
sub_to_main = dict()

def getCriteria():
    main_criteria = [main.strip() for main in (input("Enter main Criteria (comma-separated):\n").split(","))]
    sub_criteria_names = []
    criteria = dict()
    for main_criterion in main_criteria:
        sub_criteria = [sub.strip() for sub in (input(f"Enter sub-criteria of {main_criterion} (comma-separated):\n").split(","))]
        sub_criteria_names += sub_criteria
        for s in sub_criteria:
            sub_to_main[s] = main_criterion
        criteria[main_criterion] = sub_criteria
    return main_criteria, sub_criteria_names, criteria

def get_main_importance(criteria, experts):
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
    return sorted(criteria, reverse=True, key=lambda x:x[1])

def sortByImportance(main_importance, sub_importance):
    sorted_main_importance = sort(main_importance)

    sorted_sub_importance = []
    for inner_sub_importance_list in sub_importance:
        sorted_sub_importance_list = sort(inner_sub_importance_list)
        sorted_sub_importance.append(sorted_sub_importance_list)

    return sorted_main_importance, sorted_sub_importance


def get_main_sj_values(sorted_main_criteria, experts):
    """Gets sj values of every main criterion and returns dictionary of 
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
    main_sj = dict()
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
    sub_sj = dict()

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
    experts = [name.strip() for name in (input("Enter name of the experts (comma-separated):\n").split(","))]
    main_criteria, sub_criteria_names, criteria = getCriteria()

    main_importance = get_main_importance(main_criteria, experts)
    sub_importance = get_sub_importance(criteria, experts)

    sorted_main_imp, sorted_sub_imp = sortByImportance(main_importance, sub_importance)

    main_sj = get_main_sj_values(sorted_main_imp, experts)
    sub_sj = get_sub_sj_values(sorted_sub_imp, experts)


if __name__ == "__main__":
    get_inputs()
    # kj, qj
    # wj
    # get global weigths
    # sort on the basis of global weights