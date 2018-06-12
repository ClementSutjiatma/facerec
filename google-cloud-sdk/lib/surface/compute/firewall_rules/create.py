# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Command for creating firewall rules."""

from __future__ import absolute_import
from __future__ import unicode_literals
from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.api_lib.compute import firewalls_utils
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.compute.firewall_rules import flags
from googlecloudsdk.command_lib.compute.networks import flags as network_flags
from googlecloudsdk.core.console import progress_tracker


@base.ReleaseTracks(base.ReleaseTrack.GA)
class Create(base.CreateCommand):
  """Create a Google Compute Engine firewall rule."""

  with_disabled = False

  FIREWALL_RULE_ARG = None
  NETWORK_ARG = None

  @classmethod
  def Args(cls, parser):
    parser.display_info.AddFormat(flags.DEFAULT_LIST_FORMAT)
    cls.FIREWALL_RULE_ARG = flags.FirewallRuleArgument()
    cls.FIREWALL_RULE_ARG.AddArgument(parser, operation_type='create')
    cls.NETWORK_ARG = network_flags.NetworkArgumentForOtherResource(
        'The network to which this rule is attached.', required=False)
    firewalls_utils.AddCommonArgs(
        parser,
        for_update=False,
        with_egress_support=True,
        with_service_account=True,
        with_disabled=cls.with_disabled)
    firewalls_utils.AddArgsForServiceAccount(parser, for_update=False)
    parser.display_info.AddCacheUpdater(flags.FirewallsCompleter)

  def _CreateFirewall(self, holder, args):
    client = holder.client

    if args.rules and args.allow:
      raise firewalls_utils.ArgumentValidationError(
          'Can NOT specify --rules and --allow in the same request.')

    if bool(args.action) ^ bool(args.rules):
      raise firewalls_utils.ArgumentValidationError(
          'Must specify --rules with --action.')

    allowed = firewalls_utils.ParseRules(args.allow, client.messages,
                                         firewalls_utils.ActionType.ALLOW)

    network_ref = self.NETWORK_ARG.ResolveAsResource(args, holder.resources)
    firewall_ref = self.FIREWALL_RULE_ARG.ResolveAsResource(
        args, holder.resources)

    firewall = client.messages.Firewall(
        allowed=allowed,
        name=firewall_ref.Name(),
        description=args.description,
        network=network_ref.SelfLink(),
        sourceRanges=args.source_ranges,
        sourceTags=args.source_tags,
        targetTags=args.target_tags)

    firewall.direction = None
    if args.direction and args.direction in ['EGRESS', 'OUT']:
      firewall.direction = (
          client.messages.Firewall.DirectionValueValuesEnum.EGRESS)
    else:
      firewall.direction = (
          client.messages.Firewall.DirectionValueValuesEnum.INGRESS)

    firewall.priority = args.priority
    firewall.destinationRanges = args.destination_ranges

    allowed = []
    denied = []
    if not args.action:
      allowed = firewalls_utils.ParseRules(
          args.allow, client.messages, firewalls_utils.ActionType.ALLOW)
    elif args.action == 'ALLOW':
      allowed = firewalls_utils.ParseRules(
          args.rules, client.messages, firewalls_utils.ActionType.ALLOW)
    elif args.action == 'DENY':
      denied = firewalls_utils.ParseRules(
          args.rules, client.messages, firewalls_utils.ActionType.DENY)
    firewall.allowed = allowed
    firewall.denied = denied

    firewall.sourceServiceAccounts = args.source_service_accounts
    firewall.targetServiceAccounts = args.target_service_accounts
    return firewall, firewall_ref.project

  def Run(self, args):
    """Issues requests necessary for adding firewall rules."""
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())
    client = holder.client

    firewall, project = self._CreateFirewall(holder, args)
    request = client.messages.ComputeFirewallsInsertRequest(
        firewall=firewall, project=project)
    with progress_tracker.ProgressTracker('Creating firewall'):
      return client.MakeRequests([(client.apitools_client.firewalls, 'Insert',
                                   request)])


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class BetaCreate(Create):
  """Create a Google Compute Engine firewall rule."""

  with_disabled = True

  @classmethod
  def Args(cls, parser):
    parser.display_info.AddFormat(flags.DEFAULT_LIST_FORMAT_BETA)
    cls.FIREWALL_RULE_ARG = flags.FirewallRuleArgument()
    cls.FIREWALL_RULE_ARG.AddArgument(parser, operation_type='create')
    cls.NETWORK_ARG = network_flags.NetworkArgumentForOtherResource(
        'The network to which this rule is attached.', required=False)
    firewalls_utils.AddCommonArgs(
        parser,
        for_update=False,
        with_egress_support=True,
        with_service_account=True,
        with_disabled=cls.with_disabled)
    firewalls_utils.AddArgsForServiceAccount(parser, for_update=False)

  def _CreateFirewall(self, holder, args):
    firewall, project = super(BetaCreate, self)._CreateFirewall(holder, args)
    if args.disabled is not None:
      firewall.disabled = args.disabled

    return firewall, project


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class AlphaCreate(BetaCreate):
  """Create a Google Compute Engine firewall rule."""

  @classmethod
  def Args(cls, parser):
    parser.display_info.AddFormat(flags.DEFAULT_LIST_FORMAT_BETA)
    cls.FIREWALL_RULE_ARG = flags.FirewallRuleArgument()
    cls.FIREWALL_RULE_ARG.AddArgument(parser, operation_type='create')
    cls.NETWORK_ARG = network_flags.NetworkArgumentForOtherResource(
        'The network to which this rule is attached.', required=False)
    firewalls_utils.AddCommonArgs(
        parser,
        for_update=False,
        with_egress_support=True,
        with_service_account=True,
        with_disabled=cls.with_disabled)
    firewalls_utils.AddArgsForServiceAccount(parser, for_update=False)
    flags.AddEnableLogging(parser, default=None)

  def _CreateFirewall(self, holder, args):
    firewall, project = super(AlphaCreate, self)._CreateFirewall(holder, args)
    firewall.enableLogging = args.enable_logging

    return firewall, project


Create.detailed_help = {
    'brief': 'Create a Google Compute Engine firewall rule.',
    'DESCRIPTION':
        """\
        *{command}* is used to create firewall rules to allow/deny
        incoming/outgoing traffic.
        """,
    'EXAMPLES':
        """\
      To create a firewall rule allowing incoming TCP traffic on port 8080, run:

        $ {command} FooService --allow tcp:8080 \
--description "Allow incoming traffic on TCP port 8080" --direction INGRESS

      To create a firewall rule that allows TCP traffic through port 80 and
      determines a list of specific IP address blocks that are allowed to make
      inbound connections, run:

        $ {command} "tcp-rule" --allow tcp:80 \
--source-ranges="10.0.0.0/22,10.0.0.0/14" --description="Narrowing TCP traffic"

      To list existing firewall rules, run:

        $ gcloud compute firewall-rules list

      For more detailed examples see
      [](https://cloud.google.com/vpc/docs/using-firewalls)
        """,
}
