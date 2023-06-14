from plot_import import *

# three part
one_third = np.quantile(list(data['mir_score']), 0.333)
two_third = np.quantile(list(data['mir_score']), 0.666)
print("one_third:{}, two_third:{}".format(str(two_third), str(one_third)))
one_third_data = data.copy()
two_third_data = data[data['mir_score']>=one_third]
three_third_data = data[data['mir_score']>=two_third]
print("all len:{}, 2/3 len:{}, 1/3 len:{}".format(str(len(one_third_data)), str(len(two_third_data)), str(len(three_third_data))))
print("< Deletion > all len:{}, 2/3 len:{}, 1/3 len:{}".
      format(str(len(one_third_data[~one_third_data['D'].astype(str).isin(['[]'])])), 
      str(len(two_third_data[~two_third_data['D'].astype(str).isin(['[]'])])), 
      str(len(three_third_data[~three_third_data['D'].astype(str).isin(['[]'])]))))
print("< Mismatch > all len:{}, 2/3 len:{}, 1/3 len:{}".
      format(str(len(one_third_data[~one_third_data['M'].astype(str).isin(['[]'])])),
      str(len(two_third_data[~two_third_data['M'].astype(str).isin(['[]'])])),
      str(len(three_third_data[~three_third_data['M'].astype(str).isin(['[]'])]))))

# three part (三群分開)
'''
one_third = np.quantile(list(data['mir_score']), 0.333)
two_third = np.quantile(list(data['mir_score']), 0.666)
print(one_third, two_third)
one_third_data = data[data['mir_score']<one_third]
two_third_data = data[data['mir_score']>=one_third]
two_third_data = two_third_data[two_third_data['mir_score']<two_third]
three_third_data = data[data['mir_score']>=two_third]
print(len(one_third_data), len(two_third_data), len(three_third_data))
print(len(one_third_data[~one_third_data['D'].astype(str).isin(['[]'])]),
      len(two_third_data[~two_third_data['D'].astype(str).isin(['[]'])]),
      len(three_third_data[~three_third_data['D'].astype(str).isin(['[]'])]))
print(len(one_third_data[~one_third_data['M'].astype(str).isin(['[]'])]),
      len(two_third_data[~two_third_data['M'].astype(str).isin(['[]'])]),
      len(three_third_data[~three_third_data['M'].astype(str).isin(['[]'])]))
'''

# mutation distribution
# #### final ####
# # three_third_data、two_third_data、one_third_data
for mut in ['D', 'M']:
    sd = 0
    for split_data in [one_third_data, two_third_data, three_third_data]:
        sd += 1
        for rc_type in ['nor_readcount', 'nor_count']:
            #print(mut, sd, rc_type)
            mi_region = [[] for i in range(61)] 
            pair_region = [[] for i in range(61)] 
            read_region = [[] for i in range(61)]
            region = [i for i in range(41, -20, -1)]
            dash_del_num = 0
            name_list = []
            rc_list = []
            input_data = split_data.copy()
            input_data = input_data[~input_data[mut].astype(str).isin(['[]'])]
            input_data.reset_index(drop=True, inplace=True)
            input_data['hybrid_read'] = ['{}_{}'.format(input_data['regulator_name'][i], input_data['transcript_name'][i]) for i in range(len(input_data))]

            time.sleep(1)
            
            rc_mut = 0
            for i in range(len(input_data)):
                rc = input_data[rc_type][i] # nor_count、nor_readcount
                #if (int(input_data['mir_target_pos'][i].split('-')[0]) - 20)<1:
                #    init_pos = 1
                #else:
                init_pos = int(input_data['mir_target_pos'][i].split('-')[1]) + 20
                region_list = input_data['rem_tran_target_pos'][i].split('-')
                start = int(region_list[0])
                stop = int(region_list[1])
                mrns_stop = int(input_data['mRNA_len'][i])
                mut_list = [int(n) for n in eval(input_data[mut][i])]
                
                # total rc of mutation
                for dd in mut_list:
                    rc_mut += rc
                
                for j in range(61):
                    if init_pos - j <= mrns_stop and init_pos - j >= 0: # 在 mRNA內
                        if init_pos - j > stop: # 統計位點在 identified region外
                            continue
                        elif init_pos - j < start: # 統計位點在 identified region外
                            continue

                        elif init_pos - j in mut_list: # 統計位點有突變
                            d = init_pos - j # 突變絕對位置
                            d_pos = init_pos - int(d) # 相對於統計範圍1號位位置
                            len_m_from_back = int(input_data['mir_target_pos'][i].split('-')[1])-int(d)+1 # 突變相對於 binding site尾端(transcript)多少長度

                            if len_m_from_back <= 0: # 突變於 binding site外
                                pi_len_from_back = len_m_from_back
                            elif len_m_from_back > len(input_data['mir_transcript_seq'][i].replace('-', '')): # 突變於 binding site外
                                pi_len_from_back = len(input_data['mir_regulator_seq'][i].replace('-', '')) + (int(input_data['mir_target_pos'][i].split('-')[0])-int(d))
                            else:
                                s = -1
                                while s != -len_m_from_back:
                                    s -= 1
                                    if input_data['mir_transcript_seq'][i][s] == '-': # 若遇到 gap則將距離尾端的長度 +1
                                        len_m_from_back += 1
                                while input_data['mir_transcript_seq'][i][-len_m_from_back] == '-' or len_m_from_back == len(input_data['mir_transcript_seq'][i])+1:
                                    len_m_from_back += 1
                                seq_m_from_back = input_data['mir_regulator_seq'][i][-len_m_from_back:] # 上述長度所對應的 regulator序列
                                #dash_num_from_back = seq_m_from_back.count('-')
                                #print(seq_m_from_back)
                                #pi_seq_from_back = input_data['mir_regulator_seq'][i][-(len_m_from_back+dash_num_from_back):]
                                pi_seq_from_back = seq_m_from_back.replace('-', '') # 將 regulator序列中gap刪除
                                pi_len_from_back = len(pi_seq_from_back) # 即為突變的 regulator相對座標

                            try:
                                if input_data['mir_regulator_seq'][i][-len_m_from_back] != '-': #若突變對應到的不是 regulator gap則統計
                                    mi_region[20+pi_len_from_back-1].append(rc) # 突變發生位置統計
                                    pair_region[20+pi_len_from_back-1].append(input_data['hybrid_read'][i]) # 發生突變的 pair種類
                                    read_region[j].append(rc) # 涵蓋到的 identified region

                                else:#若突變對應到的是 regulator gap則不統計
                                    dash_del_num += 1
                            except: # 若是在 regulator座標以外的突變
                                try:
                                    mi_region[20+pi_len_from_back-1].append(rc)
                                    pair_region[20+pi_len_from_back-1].append(input_data['hybrid_read'][i])
                                    read_region[j].append(rc)
                                except:continue
                        else:                
                            try: # 若無突變則指統計 identified region涵蓋的次數    
                                read_region[j].append(rc)      
                            except:
                                continue
            #print('mut in dash: '+str(dash_del_num))

            mi_list = []
            pair_list = []
            total_mi_list = []
            s = 0
            for i in range(61):
                try:
                    total_mi_list.append(sum(mi_region[i]))
                    ave = sum(mi_region[i])/sum(read_region[i]) # 兩 list各位置相除 (突變 rc/identified region涵蓋 rc)
                    pair = len(list(set(pair_region[i]))) 
                except:
                    ave = 0
                    pair = 0
                mi_list.append(ave)
                pair_list.append(pair)
                #pi_ste_plus.append(ave + scipy.stats.sem(pi_region[i]))
                #pi_ste_minus.append(ave - scipy.stats.sem(pi_region[i]))
            total_mi_list = total_mi_list[::-1]
            mi_list = mi_list[::-1]
            pair_list = pair_list[::-1]
            #pi_ste_plus = pi_ste_plus[::-1]
            #pi_ste_minus = pi_ste_minus[::-1]

            fig, (ax1, ax2) = plt.subplots(2,1, sharex=True, figsize=(6, 10))

            ax1.axis([42, -21, 0, max(mi_list)*1.1])
            ax2.axis([42, -21, 0, max(total_mi_list)*1.1])
            ax1.bar(region, mi_list, color='#FFA07A', width=0.2)
            ax1.scatter(region, mi_list, color='#FFA07A', s=10)
            ax1.set_title('Mutation Distribution'+'\nN='+str(len(input_data)))
            ax1.set_ylabel('Ratio of mutation')
            ax1.axvline(x=1, c='k', linestyle='dashed', linewidth=0.5)
            ax1.axvline(x=21, c='k', linestyle='dashed', linewidth=0.5)
#             ax2.bar(region, pair_list, color='#FFA07A', width=0.2)
#             ax2.scatter(region, pair_list, color='#FFA07A', s=10)
#             ax2.set_title('Mutation Pair Distribution'+'\nN='+str(len(list(set(list(input_data['hybrid_read']))))))
#             ax2.set_ylabel('number of pair')
#             ax2.set_xlabel('pos')
#             ax2.axvline(x=1, c='k', linestyle='dashed', linewidth=0.5)
#             ax2.axvline(x=21, c='k', linestyle='dashed', linewidth=0.5)
            ax2.bar(region, total_mi_list, color='#FFA07A', width=0.2)
            ax2.scatter(region, total_mi_list, color='#FFA07A', s=10)
            #ax2.set_title('Mutation Distribution'+'\nN='+str(len(list(set(list(input_data['hybrid_read']))))))
            ax2.set_title('Mutation Distribution'+'\npercentage in site='+str(round(sum(total_mi_list[20: 41])/rc_mut, 3)*100)+' %')
            ax2.set_ylabel('number of mutation (rc)')
            ax2.set_xlabel('pos')
            ax2.axvline(x=1, c='k', linestyle='dashed', linewidth=0.5)
            ax2.axvline(x=21, c='k', linestyle='dashed', linewidth=0.5)
            
            if sd == 1:
                sd_type = 'all_data'
            elif sd == 2:  
                sd_type = 'two_third'
            elif sd == 3:
                sd_type = 'one_third'
            plt.savefig('figure/distribution_plot/{}_{}_{}_{}_miRanda.png'.format(d_name,mut,sd_type,rc_type))
            plt.clf()
            plt.close()
            gc.collect()

# pairing ratio
# pos 下有無 deletion 的 acc  (quick)
# !!! miRanda reg不用反轉
for mut in ['D', 'M']:
    sd = 0
    for split_data in [one_third_data, two_third_data, three_third_data]:
        sd += 1
        for rc_type in ['nor_readcount', 'nor_count']:
            #print(mut, sd, rc_type)
            d_acc_dict = {}
            acc_dict = {}
            data_acc = split_data.copy()
            reg_seq_len = int(max([len(n) for n in data_acc['regulator_seq']]))
            data_acc.reset_index(drop=True, inplace=True)
            del_data = data_acc[~data_acc[mut].astype(str).isin(['[]'])]
            per_data = data_acc[data_acc[mut].astype(str).isin(['[]'])]
            del_data.reset_index(drop=True, inplace=True)
            per_data.reset_index(drop=True, inplace=True)
            #print(len(per_data), len(del_data))

            match = [0]*reg_seq_len   # 此位置無 deletion的結果
            err = [0]*reg_seq_len
            dash_in_regulator = [0]*reg_seq_len
            dash_in_transcript = [0]*reg_seq_len
            num_in_this_pos = 0
            for i in range(len(per_data)): # 無突變資料統計 pairing ratio
                #print(i, end='\r')
                trans_seq = per_data['mir_transcript_seq'][i]
                reg_seq = per_data['mir_regulator_seq'][i]

                reg_seq = reg_seq[::-1]
                mir_reg_length = len(reg_seq)
                num_in_this_pos += 1
                shift_dash = 0
                rc = per_data[rc_type][i] 
                for p in range(1, mir_reg_length+1):
                    try: # transcript序列各位置的核甘酸，對上regulator序列的位置
                        if trans_seq[(mir_reg_length-p)].upper() == 'A' and reg_seq[p-1-shift_dash].upper() == 'T':
                            match[p-1-shift_dash] += rc
                        elif trans_seq[(mir_reg_length-p)].upper() == 'T' and reg_seq[p-1-shift_dash].upper() == 'A': 
                            match[p-1-shift_dash] += rc
                        elif trans_seq[(mir_reg_length-p)].upper() == 'C' and reg_seq[p-1-shift_dash].upper() == 'G': 
                            match[p-1-shift_dash] += rc
                        elif trans_seq[(mir_reg_length-p)].upper() == 'G' and reg_seq[p-1-shift_dash].upper() == 'C': 
                            match[p-1-shift_dash] += rc
                        # GU mismatch
                        elif trans_seq[(mir_reg_length-p)].upper() == 'G' and reg_seq[p-1-shift_dash].upper() == 'T': 
                            match[p-1-shift_dash] += 0.5*rc
                            err[p-1-shift_dash] += 0.5*rc
                        elif trans_seq[(mir_reg_length-p)].upper() == 'T' and reg_seq[p-1-shift_dash].upper() == 'G': 
                            match[p-1-shift_dash] += 0.5*rc
                            err[p-1-shift_dash] += 0.5*rc
                        #else
                        elif trans_seq[(mir_reg_length-p)] == '-': # transcript若遇到gap則不統計
                            dash_in_transcript[p-1-shift_dash] += rc
                        elif reg_seq[p-1-shift_dash] == '-': # regulator若遇到gap則不能增加 regulator相對座標的位置
                            dash_in_regulator[p-1-shift_dash] += rc
                            shift_dash += 1
                            reg_seq = reg_seq[:p-shift_dash] + reg_seq[p-shift_dash+1:]

                        else: # 若不配對
                            err[p-1-shift_dash] += rc

                    except:continue # miRNA長度不一，若統計範圍超過此 miRNA長度則不統計
            #print()
            for pos in range(1, reg_seq_len+1):
                d_match = [0]*reg_seq_len # 此位置有 deletion的結果
                d_err = [0]*reg_seq_len

                dash_in_regulator = [0]*reg_seq_len
                dash_in_transcript = [0]*reg_seq_len

                d_num_in_this_pos = 0

                length = len(del_data)
                #print(pos, length, end='\r')
                for i in range(length):
                    init_pos = int(del_data['mir_target_pos'][i].split('-')[1])
                    rc = del_data[rc_type][i] # nor_count、nor_readcount
                    trans_seq = del_data['mir_transcript_seq'][i]
                    reg_seq = del_data['mir_regulator_seq'][i]
                    reg_seq = reg_seq[::-1]
                    mir_reg_length = len(reg_seq)
                    if del_data[mut][i] != '[]':
                        if len(del_data['regulator_seq'][i]) >= pos: # reg_seq長度要大於等於紀錄的位置
                            D = eval(str(del_data[mut][i]))
                            for d in D: #突變要在 binding site內
                                if init_pos-int(d) >= 0 and init_pos-int(d) <= len(del_data['mir_transcript_seq'][i].replace('-', ''))-1:
                                    s = 0
                                    dash_from_back = 0
                                    while s != init_pos-int(d)+1:
                                        if del_data['mir_transcript_seq'][i][-s-1-dash_from_back] == '-': # 突變位於 transcript尾端何處
                                            dash_from_back += 1
                                        else:
                                            s += 1
                                    if len(del_data['mir_regulator_seq'][i][int(d)-init_pos-1-dash_from_back:].replace('-', '')) == pos and del_data['mir_regulator_seq'][i][int(d)-init_pos-1-dash_from_back] != '-':
                                        d_num_in_this_pos += 1 # 判斷是否為本次要統計的突變位點
                                        shift_dash = 0 # regulator上有 dash的話不能讓 regulator pos +1

                                        for p in range(1, mir_reg_length+1):
                                            #### acc    
                                            if trans_seq[(mir_reg_length-p)].upper() == 'A' and reg_seq[p-1-shift_dash].upper() == 'T':
                                                d_match[p-1-shift_dash] += rc
                                            elif trans_seq[(mir_reg_length-p)].upper() == 'T' and reg_seq[p-1-shift_dash].upper() == 'A': 
                                                d_match[p-1-shift_dash] += rc
                                            elif trans_seq[(mir_reg_length-p)].upper() == 'C' and reg_seq[p-1-shift_dash].upper() == 'G': 
                                                d_match[p-1-shift_dash] += rc
                                            elif trans_seq[(mir_reg_length-p)].upper() == 'G' and reg_seq[p-1-shift_dash].upper() == 'C': 
                                                d_match[p-1-shift_dash] += rc
                                            # GU mismatch
                                            elif trans_seq[(mir_reg_length-p)].upper() == 'G' and reg_seq[p-1-shift_dash].upper() == 'T': 
                                                d_match[p-1-shift_dash] += 0.5*rc
                                                d_err[p-1-shift_dash] += 0.5*rc
                                            elif trans_seq[(mir_reg_length-p)].upper() == 'T' and reg_seq[p-1-shift_dash].upper() == 'G': 
                                                d_match[p-1-shift_dash] += 0.5*rc
                                                d_err[p-1-shift_dash] += 0.5*rc
                                            # else
                                            elif trans_seq[(mir_reg_length-p)] == '-':
                                                dash_in_transcript[p-1-shift_dash] += rc
                                            elif reg_seq[p-1-shift_dash] == '-':        
                                                dash_in_regulator[p-1-shift_dash] += rc
                                                shift_dash += 1
                                                reg_seq = reg_seq[:p-shift_dash] + reg_seq[p-shift_dash+1:]

                                            else:
                                                #print(del_data['mir_regulator_seq'][i], del_data['mir_transcript_seq'][i], p-1-shift_dash)
                                                d_err[p-1-shift_dash] += rc

                d_acc = [d_match[i]/(d_match[i]+d_err[i]) if (d_match[i]+d_err[i])!= 0 else 0 for i in range(reg_seq_len) ] #pairing ratio
                acc = [match[i]/(match[i]+err[i]) if (match[i]+err[i]) != 0 else 0  for i in range(reg_seq_len)] 
                d_acc_dict.update({str(pos): [d_acc, d_num_in_this_pos]}) #各位點、pairing ratio、突變位於此位置的pair數
                acc_dict.update({str(pos): [acc, num_in_this_pos]})
                
            
            # single plot    
            region = [i for i in range(1, reg_seq_len+1)]
            for i in range(1,reg_seq_len+1): 
                #print(i)
                diff = [d_acc_dict[str(i)][0][j]-acc_dict[str(i)][0][j] for j in range(reg_seq_len)]
                fig, (ax1, ax2) = plt.subplots(2,1, figsize=(6,8))
                ax1.axis([reg_seq_len, 1, 0, 1])      
                ax1.plot(region,acc_dict[str(i)][0], linewidth=0.7, label='pos {}, N={}'.format(str(i), acc_dict[str(i)][1]))
                ax1.plot(region,d_acc_dict[str(i)][0], linewidth=0.7, label='Mut pos {}, N={}'.format(str(i), d_acc_dict[str(i)][1]))
                ax1.set_xticks(region)  
                ax1.set_title('Mutation (or not) match ratio')
                ax1.axvline(x=2,c='k',linestyle='dashed', linewidth=0.7)
                ax1.axvline(x=8,c='k',linestyle='dashed', linewidth=0.7)
                ax1.axvline(x=i,c='r',linestyle='dashed', linewidth=0.5)
                ax1.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))

                ax2.plot(region, diff, linewidth=0.7, label='diff (mut-all)')
                ax2.set_title('Difference (mut - all)')
                ax2.axis([21, 1, min(diff)*1.1, max(diff)*1.1]) 
                ax2.axvline(x=i,c='r',linestyle='dashed', linewidth=0.5)
                ax2.axhline(y=0,c='k', linewidth=0.5)
                ax2.set_xticks(region)
                
                if sd == 1:
                    sd_type = 'all_data'
                elif sd == 2:  
                    sd_type = 'two_third'
                elif sd == 3:
                    sd_type = 'one_third'
                    
                plt.savefig('figure/pairing_ratio_plot/plot21/{}_{}_{}_{}_{}_miRanda.png'.format(str(i),d_name,mut,sd_type,rc_type), bbox_inches='tight')
                plt.clf()
                plt.close()
                gc.collect()
            # pairing ratio V2
            region = [i for i in range(1, reg_seq_len+1)]
            diff_1nt_before = []
            diff_1nt_after = []
            diff_2nt_before = []
            diff_2nt_after = []
            diff_3nt_before = []
            diff_3nt_after = []
            diff_4nt_before = []
            diff_4nt_after = []
            diff_5nt_before = []
            diff_5nt_after = []
            diff_6nt_before = []
            diff_6nt_after = []
            diff_7nt_before = []
            diff_7nt_after = []

            diff_this_pos = []

            for i in range(1,reg_seq_len+1):
                #print(i, end='\r')
                if d_acc_dict[str(i)][1] == 0: #若統計位點 pair個數為0，則差值計做0
                    diff_this_pos.append(0)
                    if i > 1:
                        diff_1nt_before.append(0)
                    if i > 2:
                        diff_2nt_before.append(0)
                    if i > 3:
                        diff_3nt_before.append(0)
                    if i > 4:
                        diff_4nt_before.append(0)
                    if i > 5:
                        diff_5nt_before.append(0)
                    if i > 6:
                        diff_6nt_before.append(0)
                    if i > 7:
                        diff_7nt_before.append(0)

                    if i < reg_seq_len:
                        diff_1nt_after.append(0)
                    if i < reg_seq_len-1:
                        diff_2nt_after.append(0)
                    if i < reg_seq_len-2:
                        diff_3nt_after.append(0)
                    if i < reg_seq_len-3:
                        diff_4nt_after.append(0)
                    if i < reg_seq_len-4:
                        diff_5nt_after.append(0)
                    if i < reg_seq_len-5:
                        diff_6nt_after.append(0)
                    if i < reg_seq_len-6:
                        diff_7nt_after.append(0)
                else:
                    diff_this_pos.append(d_acc_dict[str(i)][0][i-1]-acc_dict[str(i)][0][i-1]) # 配對比例差值
                    if i > 1:
                        diff_1nt_before.append(d_acc_dict[str(i)][0][i-2]-acc_dict[str(i)][0][i-2])
                    if i > 2:
                        diff_2nt_before.append(d_acc_dict[str(i)][0][i-3]-acc_dict[str(i)][0][i-3])
                    if i > 3:
                        diff_3nt_before.append(d_acc_dict[str(i)][0][i-4]-acc_dict[str(i)][0][i-4])
                    if i > 4:
                        diff_4nt_before.append(d_acc_dict[str(i)][0][i-5]-acc_dict[str(i)][0][i-5])
                    if i > 5:
                        diff_5nt_before.append(d_acc_dict[str(i)][0][i-6]-acc_dict[str(i)][0][i-6])
                    if i > 6:
                        diff_6nt_before.append(d_acc_dict[str(i)][0][i-7]-acc_dict[str(i)][0][i-7])
                    if i > 7:
                        diff_7nt_before.append(d_acc_dict[str(i)][0][i-8]-acc_dict[str(i)][0][i-8])

                    if i < reg_seq_len:
                        diff_1nt_after.append(d_acc_dict[str(i)][0][i]-acc_dict[str(i)][0][i])
                    if i < reg_seq_len-1:
                        diff_2nt_after.append(d_acc_dict[str(i)][0][i+1]-acc_dict[str(i)][0][i+1])
                    if i < reg_seq_len-2:
                        diff_3nt_after.append(d_acc_dict[str(i)][0][i+2]-acc_dict[str(i)][0][i+2])
                    if i < reg_seq_len-3:
                        diff_4nt_after.append(d_acc_dict[str(i)][0][i+3]-acc_dict[str(i)][0][i+3])
                    if i < reg_seq_len-4:
                        diff_5nt_after.append(d_acc_dict[str(i)][0][i+4]-acc_dict[str(i)][0][i+4])
                    if i < reg_seq_len-5:
                        diff_6nt_after.append(d_acc_dict[str(i)][0][i+5]-acc_dict[str(i)][0][i+5])
                    if i < reg_seq_len-6:
                        diff_7nt_after.append(d_acc_dict[str(i)][0][i+6]-acc_dict[str(i)][0][i+6])
                        
            # box
            my_pal = {'minus 7':'g', 'minus 6':'g','minus 5':'g', 'minus 4':'g',
                      'minus 3':'g', 'minus 2':'g','minus 1':'g', 'current\npos':'b',
                      'plus 1':'g', 'plus 2':'g', 'plus 3':'g','plus 4':'g', 'plus 5':'g','plus 6':'g', 'plus 7':'g'}

            tmp2 = pd.DataFrame({'plus 7':pd.Series(diff_7nt_after),'plus 6':pd.Series(diff_6nt_after),
                                 'plus 5':pd.Series(diff_5nt_after),'plus 4':pd.Series(diff_4nt_after),
                                 'plus 3':pd.Series(diff_3nt_after),'plus 2':pd.Series(diff_2nt_after),
                                 'plus 1':pd.Series(diff_1nt_after),'current\npos':pd.Series(diff_this_pos),
                                 'minus 1':pd.Series(diff_1nt_before),'minus 2':pd.Series(diff_2nt_before),
                                 'minus 3':pd.Series(diff_3nt_before), 'minus 4':pd.Series(diff_4nt_before),
                                'minus 5':pd.Series(diff_5nt_before),'minus 6':pd.Series(diff_6nt_before),
                                 'minus 7':pd.Series(diff_7nt_before)})
            plt.figure(figsize = (15,6))
            ax = sns.boxplot(data=tmp2, 
                             order=['plus 7','plus 6','plus 5','plus 4','plus 3','plus 2','plus 1','current\npos',
                                    'minus 1','minus 2','minus 3','minus 4','minus 5','minus 6','minus 7',],
                             showfliers = False, width=0.5, linewidth=1, showmeans=True, palette=my_pal) 
            ax.set_ylabel('Difference', fontsize=14)
            ax.axhline(y=0,c='k', linewidth=0.7, linestyle='--')
            for p in ax.artists:
                b, o, g, a = p.get_facecolor()
                p.set_facecolor((b, o, g, 0.3))
                
            if sd == 1:
                sd_type = 'all_data'
            elif sd == 2:  
                sd_type = 'two_third'
            elif sd == 3:
                sd_type = 'one_third'
            plt.savefig('figure/pairing_ratio_plot/plot_all/{}_{}_{}_{}_miRanda.png'.format(d_name,mut,sd_type,rc_type))
            plt.clf()
            plt.close()
            gc.collect()

