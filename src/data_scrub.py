import pandas as pd
import numpy as np
import random
import emoji


def data_reading(session_filename, message_filename):
    # Session level data
    ses = pd.read_csv(session_filename)

    #Message Level Dat
    msg = pd.read_csv(message_filename)
    return ses, msg

def data_wrangling(ses, msg):
    ses.columns = [col.strip() for col in ses.columns]
    #Message Level Dat
    msg['session_id'] = msg['session_id'].astype(str)
    ses['session_id'] = ses['session_id'].astype(str)
    #column cleaning
    msg['created_at_clean'] = pd.to_datetime(msg.created_at.astype(str).str[:-4], format='%Y-%m-%d %H:%M:%S', errors='ignore')
    msg['text_readable'] = msg.sent_from +': '+ msg.text
    ses['timestamp_clean'] = pd.to_datetime(ses.timestamp.astype(str).str[:-4], format='%Y-%m-%d %H:%M:%S', errors='ignore')
    ses.loc[(ses.timestamp_clean >='2016-06-13 00:00:00') & (ses.timestamp_clean <= '2016-08-18 00:00:00'),'no_paywall'] = 1
    ses.loc[(ses.timestamp_clean >='2016-03-16 00:00:00') & (ses.timestamp_clean <= '2016-04-12 00:00:00'),'no_paywall'] = 1
    ses['no_paywall'] = ses.no_paywall.fillna(value=0)

    #merge two tables
    df_all = msg.merge(ses, on = 'session_id')
    #subset out rubric questions and take out all uncategorized sessions
    subset_cols =ses.columns[:42].append(ses.columns[-2:])
    ses_1_42 = ses[subset_cols]
    ses_1_42 = ses_1_42[-ses_1_42.consolidated_session_category.isin(['no-msg-sent', None, 'connection-issue'])]
    ses_1_42['year-month'] = ses_1_42.timestamp_clean.astype(str).str[:7]

    # New Transformations
    ses_1_42.loc[ses_1_42.consolidated_session_category == "gap-bridged", 'gb_bool'] = 1
    ses_1_42.loc[ses_1_42.consolidated_session_category != "gap-bridged", 'gb_bool'] = 0
    #Student-level data cleaning

    # V1 : All students
    #Groupbys to join
    ses_cnt_by_student = ses_1_42.groupby('student_id').count()['session_id']
    gb_cnt_by_student = ses_1_42[ses_1_42.consolidated_session_category == 'gap-bridged']\
    .groupby('student_id').count()['session_id']
    first_gb_by_student = ses_1_42[ses_1_42.consolidated_session_category == 'gap-bridged'].groupby('student_id')['timestamp_clean'].min()
    first_session_by_student = ses_1_42.groupby('student_id')['timestamp_clean'].min()
    most_used_platform_by_student = ses_1_42.groupby('student_id')['student_platform'].agg(lambda x:x.value_counts().index[0])

    #Student level data cleaning and exploration
    students = pd.DataFrame(ses_cnt_by_student).reset_index()
    gbc = pd.DataFrame(gb_cnt_by_student).reset_index()
    first_gb = pd.DataFrame(first_gb_by_student).reset_index()
    first_session = pd.DataFrame(first_session_by_student).reset_index()
    most_used_platform = pd.DataFrame(most_used_platform_by_student).reset_index()
    bridged_ts = pd.DataFrame(ses_1_42[ses_1_42.consolidated_session_category == 'gap-bridged'].groupby('student_id')['timestamp_clean'].apply(np.array)).reset_index()
    unbridged_ts = pd.DataFrame(ses_1_42[ses_1_42.consolidated_session_category != 'gap-bridged'].groupby('student_id')['timestamp_clean'].apply(np.array)).reset_index()
    last_ub = pd.DataFrame(ses_1_42[ses_1_42.consolidated_session_category != 'gap-bridged'].groupby('student_id')['timestamp_clean'].max()).reset_index()
    most_subject = pd.DataFrame(ses_1_42.groupby('student_id')['subject'].agg(lambda x:x.value_counts().index[0])).reset_index()

    #merge into students df
    students = students.merge(gbc, how = 'left' , on = 'student_id')
    students = students.merge(first_gb,how = 'left' , on = 'student_id')
    students = students.merge(last_ub ,how = 'left' , on = 'student_id')
    students = students.merge(first_session ,how = 'left' , on = 'student_id')
    students = students.merge(most_used_platform ,how = 'left' , on = 'student_id')
    students = students.merge(most_subject ,how = 'left' , on = 'student_id')
    students = students.merge(bridged_ts ,how = 'left' , on = 'student_id')
    students = students.merge(unbridged_ts ,how = 'left' , on = 'student_id')

    #rename columns
    students.columns = ['student_id', 'session_count', 'gb_count', 'first_gb', 'last_ub', 'first_session', 'most_used_platform'\
                       ,'most_subject','bridged_ts_list', 'unbridged_ts_list']

    #clean and create new columns
    students['counter'] = students['session_count']
    students['first_gb'] = students['first_gb'].fillna(value = pd.to_datetime('2017-06-29 00:00:00', format='%Y-%m-%d %H:%M:%S'))
    students = students.fillna(value=0) #Note this created cells where NA -> 1970 dt object in first_gb column
    students['gb_rate'] = 1.0*students.gb_count / students.session_count
    students['time_to_gb'] = students.first_gb - students.first_session
    students['days_to_gb'] = students.time_to_gb.astype('timedelta64[D]')
    students['days_to_gb'] = students['days_to_gb']+1 #to combat zero day in survival analysis
    students.loc[students['first_gb'] != pd.to_datetime('2017-06-29 00:00:00', format='%Y-%m-%d %H:%M:%S'), 'observed'] = 1
    students.loc[students['first_gb'] == pd.to_datetime('2017-06-29 00:00:00', format='%Y-%m-%d %H:%M:%S'), 'observed'] = 0
    students.loc[students['last_ub'] > students['first_gb'], 'unbridged_after_gb'] = 1
    students.loc[students['last_ub'] < students['first_gb'], 'unbridged_after_gb'] = 0

    # merge all student level information
    ses_1_42 = ses_1_42.merge(students, how = 'left', on = 'student_id')



    #post merge session adding
    ses_1_42['days_since_ses_1'] = (ses_1_42.timestamp_clean - ses_1_42.first_session ).astype('timedelta64[D]')
    '''
    #On hold until survival starts back up
    #V2 : Limit to at least 5 gap bridged
    students_gb5 = students[(students.gb_count > 4)]
    students_gb5['bridged_ts5'] = students_gb5['bridged_ts_list'].str[4]
    students_gb5['days_to_gb_5'] = (students_gb5.bridged_ts5 - students_gb5.first_session).astype('timedelta64[D]') + 1

    #V3 : At least 5 sessions, death defined as getting to 5 gap_bridged
    students_gb5 = students[(students.session_count > 4)]
    students_gb5['bridged_ts5'] = students_gb5['bridged_ts_list'].str[4]
    students_gb5['bridged_ts5'] = students_gb5['bridged_ts5'].fillna(value = pd.to_datetime('2017-06-29 00:00:00', format='%Y-%m-%d %H:%M:%S'))
    students_gb5.loc[students_gb5['bridged_ts5'] != pd.to_datetime('2017-06-29 00:00:00', format='%Y-%m-%d %H:%M:%S'), 'observed'] = 1
    students_gb5.loc[students_gb5['bridged_ts5'] == pd.to_datetime('2017-06-29 00:00:00', format='%Y-%m-%d %H:%M:%S'), 'observed'] = 0
    students_gb5['days_to_gb_5'] = (students_gb5.bridged_ts5 - students_gb5.first_session).astype('timedelta64[D]') + 1
    #Subseting out system msgs
    msg = msg[(msg.sent_from == 'student') | (msg.sent_from == 'tutor')]
    msg = msg.drop_duplicates(['created_at', 'text'])
    '''

    #Subseting out system msgs
    msg = msg[(msg.sent_from == 'student') | (msg.sent_from == 'tutor')]
    msg = msg.drop_duplicates(['created_at', 'text'])

    # Count total, tutor and student msg counts
    msg_count_by_ses = pd.DataFrame(msg.groupby('session_id').count()['created_at']).reset_index()
    msg_stu_count_by_ses = pd.DataFrame(msg[(msg.sent_from == 'student')].groupby('session_id').count()['created_at']).reset_index()
    msg_tut_count_by_ses = pd.DataFrame(msg[(msg.sent_from == 'tutor')].groupby('session_id').count()['created_at']).reset_index()
    msg_count_by_ses.columns = ['session_id', 'total_count_msg']
    msg_stu_count_by_ses.columns = ['session_id', 'stu_count_msg']
    msg_tut_count_by_ses.columns = ['session_id', 'tut_count_msg']

    #gone mergin'
    ses_1_42 = ses_1_42.merge(msg_count_by_ses, how = 'left', on = 'session_id')
    ses_1_42 = ses_1_42.merge(msg_stu_count_by_ses, how = 'left', on = 'session_id')
    ses_1_42 = ses_1_42.merge(msg_tut_count_by_ses, how = 'left', on = 'session_id')

    #Take text and count words and put into df to join to session master data set
    msg['text'] = msg['text'].astype(str)
    msg['text_lower'] = [t.lower() for t in msg.text]
    full_transcript_by_session = pd.DataFrame(msg[msg.content_type == 'text'].groupby('session_id')['text'].apply(list)).reset_index()
    joined_text = [" ".join(transcript) for transcript in  full_transcript_by_session.text]
    split_of_transcript = [t.split() for t in joined_text]
    length_list = [len(t) for t in split_of_transcript]
    char_list = [len(t) for t in joined_text]
    question_count_list = [t.count('?') for t in joined_text]
    msg_question_count =  [t.count('?') for t in msg.text]

    full_transcript_by_session['text'] = joined_text
    full_transcript_by_session['word_count'] = length_list
    full_transcript_by_session['char_count'] = char_list
    full_transcript_by_session['question_count'] = question_count_list
    ses_1_42 = ses_1_42.merge(full_transcript_by_session, how = 'left', on = 'session_id')

    ques_start = ['how', 'what', 'when' , 'where' , 'why', 'who']
    for word in ques_start:
        _ls_start = [t.strip()[:len(word)].count(word) for t in msg.text_lower]
        _ls_any = [t.count(word) for t in msg.text_lower]
        msg[word + '_start'] = _ls_start
        msg[word + '_any'] = _ls_any

    def emoji_list_search(ls):
        for item in ls:
            if unicode(item, 'utf-8') in emoji.UNICODE_EMOJI:
                return 1.0
        return 0.0

    lower_msg_split = [t.split() for t in msg.text_lower]
    msg["emoji_bool"] = [emoji_list_search(ls) for ls in lower_msg_split]

    msg['question_student_count'] = np.array([1 if t.count("?")>0 else 0 for t in msg.text_lower])
    msg['first_word'] = [ None if t.split()==[] else t.split()[0] for t in msg.text_lower]

    sum_msg_vars = ['how_start', 'what_start', 'when_start' , 'where_start' , 'why_start', 'who_start',\
                        'how_any', 'what_any', 'when_any' , 'where_any' , 'why_any', 'who_any',\
                       'emoji_bool']
    ques_start_any = []
    #merging question start counts for start of msg and anywhere in message
    ses_1_42 = ses_1_42.merge(pd.DataFrame(msg[(msg.sent_from == 'student')].groupby('session_id')[sum_msg_vars].sum()).reset_index(), how = 'left', on = 'session_id')
    ses_1_42 = ses_1_42.merge(pd.DataFrame(msg[(msg.sent_from == 'student')].groupby('session_id')['question_student_count'].sum()).reset_index(), how = 'left', on = 'session_id')

    ses_1_42['high_level'] = ses_1_42['why_any'] + ses_1_42['how_any']
    ses_1_42['low_level'] = ses_1_42['where_any'] + ses_1_42['when_any'] + ses_1_42['what_any'] + ses_1_42['who_any']
    ses_1_42['high_level_ratio'] = ses_1_42['high_level'] / pd.Series([1.0 if num == 0.0 else num for num in ses_1_42.low_level])
    #Note missing values found here -> #ses_1_42[(pd.isnull(ses_1_42.word_count))
    #no message data for 5K sessions
    # here are gb with no msg data: ses_1_42[(pd.isnull(ses_1_42.word_count)) &\(ses_1_42.consolidated_session_category == 'gap-bridged')]['session_id']
    #All the sessions without missing message data
    # some may be no stud msg, connection isuue, etc
    ses_full = ses_1_42[(pd.notnull(ses_1_42.word_count))]
    ses_full['ses_num_order'] = ses_full.groupby('student_id').cumcount()
    ses_full['ses_num_order'] = ses_full['ses_num_order'] + 1

    #This creates incompleteness here as well
    #to correct I'll filter out all student ids that appear in sessions without message data
    students_full = students[-students.student_id.isin(ses_1_42[pd.isnull(ses_1_42.word_count)]['student_id'])]

    #merging student session group by to apprpriate stduent population
    students_full = students_full.merge(pd.DataFrame(ses_full.groupby('student_id')['question_student_count'].sum()).reset_index(), how = 'left', on = 'student_id')

    students_full['question_student_count_ratio'] = 1.0*students_full['question_student_count'] / students_full['session_count']

    #subsetting some invalid sessions without msg data
    ses_full = ses_full[-ses_full.question_student_count.isnull()]
    # lower case text
    ses_full['text'] = ses_full.text.str.lower()

    #suggested growth mindset phrases
    gm_phrase = ['hard work', 'working hard',"you're so close", 'you are so close', 'nice effort', 'good job', \
                 "you've got this", "you got this", "keep at it", "keep going", "keep trying", "almost there", "yet"]

    #individually inputting phrases
    for i, phrase in enumerate(gm_phrase):
        _ls_any = [1 if t.count(phrase)> 0 else 0 for t in msg.text_lower.astype(str)]
        msg['gp_' + str(i)] = _ls_any


    ses_full = ses_full.merge(pd.DataFrame(msg[(msg.sent_from == 'tutor')].groupby('session_id')[msg.columns[-13:]].sum()).reset_index(), how = 'left', on = 'session_id')


    #summing across rows and than a boolean for gp preasent
    ses_full['gp_sum'] = ses_full[ses_full.columns[-13:]].sum(axis = 1)
    ses_full.loc[ ses_full.gp_sum > 0 , 'gp_bool']  =  1
    ses_full.loc[ ses_full.gp_sum == 0 , 'gp_bool']  =  0


    min_ses_df = pd.DataFrame(msg.groupby('session_id')['created_at_clean'].min()).reset_index()
    max_ses_df = pd.DataFrame(msg.groupby('session_id')['created_at_clean'].max()).reset_index()
    df_diff = min_ses_df.merge(max_ses_df, how = 'left', on = 'session_id')
    df_diff['created_at_clean_y']  = pd.to_datetime(df_diff['created_at_clean_y'], format='%Y-%m-%d %H:%M:%S', errors='ignore')
    df_diff['created_at_clean_x']  = pd.to_datetime(df_diff['created_at_clean_x'], format='%Y-%m-%d %H:%M:%S', errors='ignore')
    df_diff['ses_time_delta'] = (df_diff['created_at_clean_y'] - df_diff['created_at_clean_x']).astype('timedelta64[m]')
    ses_full = ses_full.merge(df_diff, how = 'left', on = "session_id")

    # Canned Response feature engineering
    cr = pd.read_csv("data/canned_resp.csv")
    text_fail_lower = cr.text_fail.str.lower().unique()
    text_probe_lower = cr.text_probe.str.lower().unique()[:-1]
    text_begin_lower = cr.text_begin.str.lower().unique()[:-1]

    for i, phrase in enumerate(text_fail_lower):
        _ls_any = [1 if t.count(phrase)> 0 else 0 for t in msg.text_lower.astype(str)]
        msg['crf_' + str(i)] = _ls_any
    ses_full = ses_full.merge(pd.DataFrame(msg[(msg.sent_from == 'tutor')].groupby('session_id')[msg.columns[-len(text_fail_lower):]].sum()).reset_index(), how = 'left', on = 'session_id')
    ses_full['crf_sum'] = ses_full[ses_full.columns[-len(text_fail_lower):]].sum(axis=1)

    for i, phrase in enumerate(text_probe_lower):
        _ls_any = [1 if t.count(phrase)> 0 else 0 for t in msg.text_lower.astype(str)]
        msg['crp_' + str(i)] = _ls_any
    ses_full = ses_full.merge(pd.DataFrame(msg[(msg.sent_from == 'tutor')].groupby('session_id')[msg.columns[-len(text_probe_lower):]].sum()).reset_index(), how = 'left', on = 'session_id')
    ses_full['crp_sum'] = ses_full[ses_full.columns[-len(text_probe_lower):]].sum(axis=1)

    for i, phrase in enumerate(text_begin_lower):
        _ls_any = [1 if t.count(phrase)> 0 else 0 for t in msg.text_lower.astype(str)]
        msg['crb_' + str(i)] = _ls_any
    ses_full = ses_full.merge(pd.DataFrame(msg[(msg.sent_from == 'tutor')].groupby('session_id')[msg.columns[-len(text_begin_lower):]].sum()).reset_index(), how = 'left', on = 'session_id')
    ses_full['crb_sum'] = ses_full[ses_full.columns[-len(text_begin_lower):]].sum(axis=1)

    #student name count/dataframe variant
    s_meta = pd.read_csv("data/student_user_table.csv")
    s_meta = s_meta[['User Id', 'First Name']]
    s_meta.columns = ['student_id' , 'first_name']
    ses_full = ses_full.merge(s_meta, how = 'left', on = 'student_id')
    ses_full_student = ses_full[-pd.isnull(ses_full.first_name)]

    ses_full_student['first_name'] = ses_full_student.first_name.str.lower()
    names = ses_full_student.first_name.values
    text = ses_full_student.text.values
    name_count = []
    for tup in zip(names, text):
        name_count.append(tup[1].count(tup[0]))

    ses_full_student['name_count'] = name_count
    ses_full_student['name_rate'] = ses_full_student.name_count / ses_full_student.word_count
    
    return ses_1_42, ses_full, students, students_full, msg


ses, msg = data_reading("/Users/ricky/yup-capstone/data/yup-sessions-2017-06-29.csv", "/Users/ricky/yup-capstone/data/yup-messages-complete.csv")
ses_1_42, ses_full, students, students_full, msg = data_wrangling(ses, msg)


df_name_list = ['ses_1_42', 'ses_full', 'students', 'students_full', 'msg']
for i, df in enumerate([ses_1_42, ses_full, students, students_full, msg]):
    df.to_csv('/Users/ricky/yup-capstone/data/' + df_name_list[i] + ".csv")
