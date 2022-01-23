from pyverless import Resource, ResourceGroup


class DbAlarm:
    def __init__(self, sls_framework, db_name, db_arn, sns_alarm, cpu_threshold=90, memory_threshold="1000"):
        rg = ResourceGroup(sls_framework, "db_alarms")
        Resource(
            rg,
            f"{db_name}_db_cpu_alarm",
            Type="AWS::CloudWatch::Alarm",
            Properties=dict(
                AlarmDescription=f"CPU Utilization Alarm for {db_name}",
                Namespace=f"AWS/RDS",
                MetricName=f"CPUUtilization",
                Unit="Percent",
                Statistic="Average",
                Period=60,
                EvaluationPeriods=3,
                Threshold=cpu_threshold,
                TreatMissingData="breaching",
                ComparisonOperator="GreaterThanOrEqualToThreshold",
                Dimensions=[
                    dict(Name="DBInstanceIdentifier", Value=db_arn)
                ],
                AlarmActions=[]
            )
        )
        Resource(
            rg,
            f"{db_name}_db_freeable_memory_alarm",
            Type="AWS::CloudWatch::Alarm",
            Properties=dict(
                AlarmDescription=f"CPU Utilization Alarm for {db_name}",
                Namespace=f"AWS/RDS",
                MetricName=f"FreeableMemory",
                Unit="Bytes",
                Statistic="Average",
                Period=60,
                EvaluationPeriods=3,
                Threshold=memory_threshold,
                TreatMissingData="breaching",
                ComparisonOperator="LessThanOrEqualToThreshold",
                Dimensions=[
                    dict(Name="DBInstanceIdentifier", Value=db_arn)
                ],
                AlarmActions=[sns_alarm]
            )
        )
