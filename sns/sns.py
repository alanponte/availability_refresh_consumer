import json
from typing import Dict

import boto3

from logger import get_logger

_LOGGER = get_logger()

SNS_CLIENT = boto3.client('sns')

# todo: What should this be?
# https://www.repost.aws/questions/QUidOETC17R2Cf5vTawtgBpA/questions/QUidOETC17R2Cf5vTawtgBpA/can-someone-explain-the-point-of-messagegroupid?
DEFAULT_MESSAGE_GROUP_ID = '1'


class SNS:
    """Wrapper around S3 Operations."""
    def __init__(self, topic_arn: str):
        self._sns_client = SNS_CLIENT
        self._topic_arn = topic_arn

    def publish(self, subject: str, message: Dict) -> Dict:
        """Publish the message to SNS topic

        :param subject: Subject of the message.
        :param message: Message body.
        :return: The response dict from AWS
        """
        try:
            response = self._sns_client.publish(
                TopicArn=self._topic_arn,
                Subject=subject,
                Message=json.dumps(message),
                MessageGroupId=DEFAULT_MESSAGE_GROUP_ID,
                # todo: What should this parameter be?
                # https://stackoverflow.com/questions/62655047/aws-sqs-fifo-queue-the-queue-should-either-have-contentbaseddeduplication-enabl
                MessageDeduplicationId='1'
            )
            return response
        except Exception as e:
            message = f'Encountered exception while publishing SNS message to {self._topic_arn}'
            _LOGGER.info(message)
