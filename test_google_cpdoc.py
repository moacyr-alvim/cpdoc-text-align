import nwalgorithm
import re
import time
import numpy as np

M = 1
MM = -1
IS = -1
IB = -1

f = open("Entrevistas/2347_carlos_santos_cruz_2016-10-21_01.txt", 'r')
transcricao_humana = f.read()

transcricao_humana = transcricao_humana[1:]
transcricao_humana = re.sub('\n', ' ', transcricao_humana)
transcricao_humana = re.sub('B. L. – ', '', transcricao_humana)
transcricao_humana = re.sub('S. C. – ', '', transcricao_humana)
transcricao_humana = re.sub('M. T. – ', '', transcricao_humana)
transcricao_humana = re.sub(r'[^\w\s]', '', transcricao_humana)
transcricao_humana = re.sub('  ', ' ', transcricao_humana)
transcricao_humana =transcricao_humana.lower()

f = open("transcription/transcricao-2347_carlos_santos_cruz_2016-10-21_01.txt", 'r')
transcricao_maquina = f.read()

transcricao_maquina = transcricao_maquina.split("Transcript:")
transcricao_maquina = [i.split('\nconfidence:')[0].strip() for i in transcricao_maquina if i != '']

transcricao_maquina = ' '.join(transcricao_maquina)

len_maquina_letter = len(transcricao_maquina)

transcricao_maquina = transcricao_maquina.lower()

sample_1, sample_2, nw_matrix, caminho, duration = nwalgorithm.best_align(transcricao_humana,transcricao_maquina, M,MM,IS,IB)

print(sample_1)
print(sample_2)
print(duration)

len(sample_1)
len(sample_2)

print(nw_matrix)

f = open("transcription/transcricao-2347_carlos_santos_cruz_2016-10-21_01.txt", 'r')
transcricao_maquina = f.read()
transcricao_maquina = transcricao_maquina.split("Word:")
transcricao_maquina = [i.split('\nTranscript:')[0].strip() for i in transcricao_maquina[1:] if i != '']

#mean_time_letter = round(dic_pos_time[len(dic_pos_time)-1]['end_time']/len_maquina_letter,1)

def phrase_dic(phrase, list_word_time):
    phrase = phrase.split()
    dic = {}

    j = 0
    for i in range(0,len(phrase)):
        if phrase[i] == '':
            pass
            j=j-1
        else:
            if '#' in phrase[i]:
                word = len(phrase[i])+1

                start_time = dic[i-1]['end_time']
                end_time = np.round(dic[i-1]['end_time']+word*0.06,1)

                dic.update({i: {'start_time': float(start_time), 'end_time': float(end_time), 'word': phrase[i]}})
                j = j - 1
            else:
                start_time = re.search('start_time: (\d+\.\d+)', list_word_time[i+j]).group(1)
                end_time = re.search('end_time: (\d+\.\d+)', list_word_time[i+j]).group(1)
                dic.update({i: {'start_time': float(start_time), 'end_time': float(end_time), 'word': phrase[i]}})

    return dic

dic_pos_time = phrase_dic(sample_1,transcricao_maquina)

transcricao_humana_align = sample_2.split()
phrase = sample_1.split()

mean_time_word = np.mean([dic_pos_time[i]['end_time']-dic_pos_time[i]['start_time'] for i in dic_pos_time])
sd_time_word = np.std([dic_pos_time[i]['end_time']-dic_pos_time[i]['start_time'] for i in dic_pos_time])


file = open("2347_carlos_santos_cruz_2016-10-21_01_v{}{}{}{}.srt".format(str(M),str(MM),str(IS),str(IB)), "w")

i = 0
j = 0

while i <= len(transcricao_humana_align):
    file.write(str(i+1) + '\n')

    if i == 0:
        start_time = dic_pos_time[i]['start_time']
        start_time_format = time.strftime('%H:%M:%S,', time.gmtime(start_time)) + \
                            re.findall('\.\d', str(start_time))[0][1] + \
                            '00'

        end_time = dic_pos_time[i]['end_time']
        end_time_format = time.strftime('%H:%M:%S,', time.gmtime(end_time)) + \
                          re.findall('\.\d', str(end_time))[0][1] + \
                          '00'

        file.write(start_time_format + ' --> ' + end_time_format + '\n')
        file.write(transcricao_humana_align[i] + '\n\n')

        i=i+1


    elif i+j >= len(transcricao_humana_align):
        start_time = dic_pos_time[i-1]['end_time']
        start_time_format = time.strftime('%H:%M:%S,', time.gmtime(start_time)) + \
                            re.findall('\.\d', str(start_time))[0][1] + \
                            '00'

        end_time = dic_pos_time[len(transcricao_humana_align)-1]['end_time']
        end_time_format = time.strftime('%H:%M:%S,', time.gmtime(end_time)) + \
                          re.findall('\.\d', str(end_time))[0][1] + \
                          '00'

        file.write(start_time_format + ' --> ' + end_time_format + '\n')
        file.write(' '.join(transcricao_humana_align[i:len(transcricao_humana_align)]) + '\n\n')

        break

    else:
        start_time = dic_pos_time[i-1]['end_time']
        start_time_format = time.strftime('%H:%M:%S,', time.gmtime(start_time)) + \
                            re.findall('\.\d', str(start_time))[0][1] + \
                            '00'

        aux = 0
        aux_pos_2 = False

        for j in range(10, 200):
            if '#' not in phrase[i+j]:
                end_time = dic_pos_time[i+j]['end_time']
                duration = end_time - start_time

                if duration == 0:
                    continue
                else:
                    length_char = len(' '.join(transcricao_humana_align[i:i+j+1]))

                    if length_char/duration <= 21 and length_char/duration >= 5:
                        pos_2 = j
                        aux_pos_2 = True
                        break
                    elif aux < length_char/duration:
                        aux = length_char/duration
                        pos = j

        if aux_pos_2 == True:
            j = pos_2
        else:
            j = pos


        end_time = dic_pos_time[i+j]['end_time']
        end_time_format = time.strftime('%H:%M:%S,', time.gmtime(end_time)) + \
                          re.findall('\.\d', str(end_time))[0][1] + \
                          '00'

        temp_phrase = ' '.join(transcricao_humana_align[i:i + j + 1])
        number_of_word = len(temp_phrase.split())

        if number_of_word > 30:
            total_time = end_time - start_time
            time_per_word = total_time/number_of_word

            number_partition = int(np.ceil(number_of_word/30))
            size_partition = int(np.ceil(number_of_word/number_partition))

            for part in range(0, number_partition):

                if part == number_partition-1:

                    new_start_time_format = new_end_time_format

                    new_phrase = ' '.join(temp_phrase.split()[part*size_partition:number_of_word])

                    file.write(new_start_time_format + ' --> ' + end_time_format + '\n')
                    file.write(new_phrase + '\n\n')

                elif part == 0:

                    new_end_time = np.round(start_time + size_partition*time_per_word, 1)

                    new_end_time_format = time.strftime('%H:%M:%S,', time.gmtime(new_end_time)) + \
                                      re.findall('\.\d', str(new_end_time))[0][1] + \
                                      '00'

                    new_phrase = ' '.join(temp_phrase.split()[0:size_partition])

                    file.write(start_time_format + ' --> ' + new_end_time_format + '\n')
                    file.write(new_phrase + '\n\n')

                else:
                    new_start_time = new_end_time
                    new_end_time = new_end_time = np.round(new_start_time + size_partition*time_per_word, 1)

                    new_start_time_format = new_end_time_format

                    new_end_time_format = time.strftime('%H:%M:%S,', time.gmtime(new_end_time)) + \
                                          re.findall('\.\d', str(new_end_time))[0][1] + \
                                          '00'

                    new_phrase = ' '.join(temp_phrase.split()[part*size_partition:part*size_partition+size_partition])

                    file.write(new_start_time_format + ' --> ' + new_end_time_format + '\n')
                    file.write(new_phrase + '\n\n')

        else:
            file.write(start_time_format + ' --> ' + end_time_format + '\n')
            file.write(temp_phrase + '\n\n')

        i=i+j+1

file.close()

print(sample_1)
print(sample_2)
print(dic_pos_time)