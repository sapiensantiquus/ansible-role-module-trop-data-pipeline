# ansible-role-module-data-pipeline
This role-module uses troposphere to generate an AWS data pipeline. The module converts YAML structured data into Troposphere native code. There are no custom mappings of fields or object names.

Troposphere code found data pipeline can be found here here:
https://github.com/cloudtools/troposphere/blob/master/troposphere/datapipeline.py

AWS Documentation for defining a data pipeline with parameterized templates can be found here:
http://docs.aws.amazon.com/datapipeline/latest/DeveloperGuide/dp-custom-templates.html

## Requirements
tested with:
- troposphere==1.6.0
- ansible==2.1.0
- boto3==1.4.1
- boto==2.43.0

## Example playbook

```
- hosts: test
  vars:
    data_pipeline_stack_name: "test-data-pipline"
    data_pipeline:
      PipelineObjects:
        - Name: "ShellCommandActivityObj"
          Id: "ShellCommandActivityObj"
          Fields:
            - Key: "type"
              StringValue: "ShellCommandActivity"
            - Key: "schedule"
              RefValue: "Schedule"
            - Key: "command"
              StringValue: "#{myShellCmd}"
            - Key: "runsOn"
              RefValue: "EC2ResourceObj"
        - Name: "EC2ResourceObj"
          Id: "EC2ResourceObj"
          Fields:
            - Key: "instanceType"
              StringValue: "t2.micro"
            - Key: "type"
              StringValue: "Ec2Resource"
            - Key: "role"
              StringValue: "DataPipelineDefaultRole"
            - Key: "resourceRole"
              StringValue: "DataPipelineDefaultResourceRole"
        - Id: "Schedule"
          Name: "Schedule"
          Fields:
            - Key: "occurrences"
              StringValue: "4"
            - Key: "startAt"
              StringValue: "FIRST_ACTIVATION_DATE_TIME"
            - Key: "type"
              StringValue: "Schedule"
            - Key: "period"
              StringValue: "15 minutes"
      ParameterObjects:
        - Id: "myShellCmd"
          Attributes:
            - Key: "description"
              StringValue: "Shell command to run"
            - Key: "type"
              StringValue: "String"
            - Key: "default"
              StringValue: "ls -l"
      ParameterValues:
        - Id: "myShellCmd"
          StringValue: "ls -l /"
  roles:
    - ansible-role-module-data-pipeline
```
