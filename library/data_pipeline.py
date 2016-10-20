#!/usr/bin/env python
from troposphere import datapipeline, Template
import boto3
from ansible.module_utils.basic import *

def build_pipeline_object(pipeline_object):
    fields = [datapipeline.ObjectField("objField",**ansible_field) for ansible_field in pipeline_object['Fields']]
    del pipeline_object['Fields']
    obj = datapipeline.PipelineObject(pipeline_object['Name'],Fields=fields,**pipeline_object)
    return obj

def build_pipeline_parameter_object(ansible_parameter_object):
        parameter_object = datapipeline.ParameterObject(
            Attributes=[datapipeline.ParameterObjectAttribute(**attribute) for attribute in ansible_parameter_object['Attributes']],
            Id=ansible_parameter_object['Id']
        )
        return parameter_object

def build_pipeline(ansible_pipeline):
    pipeline = datapipeline.Pipeline(
        "datapipeline",
        Name="Pipeline",
        PipelineObjects=[build_pipeline_object(ansible_pipeline_object) for ansible_pipeline_object in ansible_pipeline['PipelineObjects']]
    )

    if 'ParameterObjects' in ansible_pipeline:
        pipeline.ParameterObjects = [build_pipeline_parameter_object(obj) for obj in ansible_pipeline['ParameterObjects']]

    if 'ParameterValues' in ansible_pipeline:
        pipeline.ParameterValues = [datapipeline.ParameterValue(**value) for value in ansible_pipeline['ParameterValues']]

    if 'PipelineTags' in ansible_pipeline:
        pipeline.PipelineTags = [datapipeline.PipelineTags(**tag) for tag in ansible_pipeline['PipelineTags']]

    return pipeline



def main():
    cfn = boto3.client('cloudformation',region_name='us-west-2')
#    cfn.list_stacks()
    global module
    module = AnsibleModule(
        argument_spec = dict(
          data_pipeline  = dict(required=True, type='dict')
        )
    )
    data_pipeline = module.params.get('data_pipeline')
    template = Template()

    pipeline = build_pipeline(data_pipeline)
    template.add_resource(pipeline)

    module.exit_json(
        Changed=False,
        Failed=False,
        Result=template.to_json()
    )

if __name__ == "__main__":
    main()
