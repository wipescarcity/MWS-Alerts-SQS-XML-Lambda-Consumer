
import boto3
import os
import logging
import json
import xmltodict

#Uses xmltodict by martinblech (https://github.com/martinblech/xmltodict) to parse xml into json
#xmltodict is distributed under the MIT license which allows commercial and private use, distribution and modification


# create logger (logs can be found in CloudWatch)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

# get function environmental variables
MWSQUEUE = os.environ.get('MWSQUEUE')
MWSMAXMSG =  int(os.environ.get('MWSMAXMSG'))
MWSTOPIC = os.environ.get('MWSTOPIC')

def lambda_handler(event, context):

    # uncomment to output function event and context to logs
    #if context:
    #    LOGGER.debug('Function ARN: %s', context.invoked_function_arn)
    #else:
    #    LOGGER.warning('Lambda context is missing')    
    LOGGER.info(json.dumps(event))

    # create  sqs service resource 
    sqs = boto3.resource('sqs')
    
    # get queue 
    queue = sqs.Queue(MWSQUEUE)
    LOGGER.info('created queue')
    eventXMLbody = event['Records'][0]['body']
    LOGGER.info('XML Payload:')
    LOGGER.info(eventXMLbody)
    parsedDict = xmltodict.parse(eventXMLbody)
    dictDump = json.dumps(parsedDict)
    LOGGER.info('JSON dump:')
    LOGGER.info(dictDump)
    
    # This is how to actively receive SQS messages
    #parse xml messages and print xml and json versions to log
    #for message in queue.receive_messages(MaxNumberOfMessages=MWSMAXMSG):
        #LOGGER.info('receiving messages...')
        #parse xml string to json and then to string
        #msgdict = xmltodict.parse(message.body)
        #dictdump = json.dumps(msgdict)
        
        #output data to log
        #LOGGER.info('__________________________________________')
        #LOGGER.info('Message ID:')
        #LOGGER.info(message.message_id)
        #LOGGER.info('Message Body in XML:')
        #LOGGER.info(message.body)
        #LOGGER.info('Message Body as a dict:')
        #LOGGER.info(dictdump)
        #LOGGER.info('__________________________________________')
    
        # Let the queue know that the message is processed
        #message.delete()
            
    # Get the SNS resource
    sns = boto3.resource('sns')
    
     # Get the queue
    topic = sns.Topic(MWSTOPIC)
    
    #Send results to topic
    response = topic.publish(
        Subject='MWS Alert',
        Message=dictDump
    )