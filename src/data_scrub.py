import pandas as pd
import numpy as np
import random


def data_reading(session_filename, message_filename):
    # Session level data
    ses = pd.read_csv(session_filename)

    #Message Level Dat
    msg = pd.read_csv(message_filename)
    return ses, msg

def data_wrangling(ses, msg):
    ses.columns = [col.strip() for col in ses.columns]
    #column cleaning
    msg['created_at_clean'] = pd.to_datetime(msg.created_at.astype(str).str[:-4], format='%Y-%m-%d %H:%M:%S', errors='ignore')
    msg['text_readable'] = msg.sent_from +': '+ msg.text
    ses['timestamp_clean'] = pd.to_datetime(ses.timestamp.astype(str).str[:-4], format='%Y-%m-%d %H:%M:%S', errors='ignore')
    #merge two tables
    df_all = msg.merge(ses, on = 'session_id')
    #subset out rubric questions and take out all uncategorized sessions
    subset_cols =ses.columns[:42].append(ses.columns[-1:])
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

    ques_start = ['how', 'what', 'when' , 'where' , 'why', 'can']
    for word in ques_start:
        _ls = [t.strip()[:len(word)].count(word) for t in msg.text_lower]
        msg[word] = _ls

    #merging question start counts to sessions
    msg['question_student_count'] = np.array([t.count("?") for t in msg.text_lower])
    msg['first_word'] = [ None if t.split()==[] else t.split()[0] for t in msg.text_lower]
    ses_1_42 = ses_1_42.merge(pd.DataFrame(msg.groupby('session_id')[ques_start].sum()).reset_index(), how = 'left', on = 'session_id')
    #This turns question start + "_x" into a count of all question starts and question start + "_y" into just student questions
    ses_1_42 = ses_1_42.merge(pd.DataFrame(msg[(msg.sent_from == 'student')].groupby('session_id')[ques_start].sum()).reset_index(), how = 'left', on = 'session_id')
    ses_1_42 = ses_1_42.merge(pd.DataFrame(msg[(msg.sent_from == 'student')].groupby('session_id')['question_student_count'].sum()).reset_index(), how = 'left', on = 'session_id')
    #Note missing values found here -> #ses_1_42[(pd.isnull(ses_1_42.word_count))
    #no message data for 5K sessions
    #All the sessions without missing message data
    ses_full = ses_1_42[(pd.notnull(ses_1_42.word_count))]
    #This creates incompleteness here as well
    #to correct I'll filter out all student ids that appear in sessions without message data
    students_full = students[-students.student_id.isin(ses_1_42[pd.isnull(ses_1_42.word_count)]['student_id'])]

    #merging student session group by to apprpriate stduent population
    students_full = students_full.merge(pd.DataFrame(ses_full.groupby('student_id')['question_student_count'].sum()).reset_index(), how = 'left', on = 'student_id')

    students_full['question_student_count_ratio'] = 1.0*students_full['question_student_count'] / students_full['session_count']
    ses_full['ses_num_order'] = ses_full.groupby('student_id').cumcount()


    return ses_1_42, ses_full, students, students_full, msg

ses, msg = data_reading("/Users/ricky/yup-capstone/data/yup-sessions-2017-06-29.csv", "/Users/ricky/yup-capstone/data/yup-messages-2017-06-29.csv")
ses_1_42, ses_full, students, students_full, msg = data_wrangling(ses, msg)

for df in ses_1_42, ses_full, students, students_full, msg:
    df.to_csv('/Users/ricky/yup-capstone/data/' + str(df))
