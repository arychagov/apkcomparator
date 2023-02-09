import xml.etree.ElementTree as ElementTree

from utils.stringify import stringify


def namespaced(attr):
    return '{http://schemas.android.com/apk/res/android}' + attr


TAG_MANIFEST = 'manifest'
TAG_APPLICATION = 'application'
TAG_PERMISSION = 'permission'
TAG_SUPPORTS_GL_TEXTURE = 'supports-gl-texture'
TAG_COMPATIBLE_SCREENS = 'compatible-screens'
TAG_SUPPORTS_SCREENS = 'supports-screens'
TAG_USES_CONFIGURATION = 'uses-configuration'
TAG_USES_FEATURE = 'uses-feature'
TAG_USES_PERMISSION = 'uses-permission'
TAG_USES_PERMISSION_SDK_23 = 'uses-permission-sdk-23'
TAG_USES_SDK = 'uses-sdk'
ATTR_NAMESPACED_NAME = namespaced('name')


def _compare_and_print(lhs: object, rhs: object, description: str, lines: list[str]):
    if isinstance(lhs, set) and isinstance(rhs, set):
        if lhs != rhs:
            lines.append('Different {}:'.format(description))
            added = rhs - lhs
            removed = lhs - rhs
            if added:
                lines.append('\tAdded: {}'.format(' '.join(list(added))))
            if removed:
                lines.append('\tRemoved: {}'.format(' '.join(list(removed))))
    elif lhs != rhs:
        lines.append('Different {}:\n\tWas: {}\n\tNow: {}'.format(description, lhs, rhs))


def _parse_names_by_tag(tree: ElementTree.Element, tag: str):
    result = set()
    for element in tree.findall(tag):
        name = element.attrib.get(ATTR_NAMESPACED_NAME, None)
        if name:
            result.add(name)
    return result


@stringify
class Application(object):
    #
    # https://developer.android.com/guide/topics/manifest/manifest-element
    #
    services = None
    activities = None
    activity_aliases = None
    providers = None
    receivers = None
    meta_datas = None

    def __init__(self, tree: ElementTree.Element):
        if tree.tag != TAG_APPLICATION:
            raise RuntimeError(
                'Expected <{}> as root tag'.format(TAG_APPLICATION))
        self.services = _parse_names_by_tag(tree, 'service')
        self.activities = _parse_names_by_tag(tree, 'activity')
        self.activity_aliases = _parse_names_by_tag(tree, 'activity-alias')
        self.providers = _parse_names_by_tag(tree, 'provider')
        self.receivers = _parse_names_by_tag(tree, 'receiver')
        self.meta_datas = _parse_names_by_tag(tree, 'meta-data')

    def print_diff(self, other, lines):
        _compare_and_print(self.services, other.services, 'services', lines)
        _compare_and_print(self.activities, other.activities, 'activities', lines)
        _compare_and_print(self.activity_aliases, other.activity_aliases, 'activity-aliases', lines)
        _compare_and_print(self.providers, other.providers, 'content providers', lines)
        _compare_and_print(self.receivers, other.receivers, 'broadcast receivers', lines)
        _compare_and_print(self.meta_datas, other.meta_datas, 'meta-datas', lines)


@stringify
class SupportsScreens(object):
    #
    # https://developer.android.com/guide/topics/manifest/supports-screens-element
    #
    resizeable = None
    small_screens = None
    normal_screens = None
    large_screens = None
    xlarge_screens = None
    any_density = None
    requires_smallest_width_dp = None
    compatible_width_limit_dp = None
    largest_width_limit_dp = None

    def __init__(self, tree: ElementTree.Element):
        if tree.tag != TAG_SUPPORTS_SCREENS:
            raise RuntimeError(
                'Expected <{}> as root tag'.format(TAG_SUPPORTS_SCREENS))
        self.resizeable = tree.attrib.get(namespaced('resizeable'), None)
        self.small_screens = tree.attrib.get(namespaced('smallScreens'), None)
        self.normal_screens = tree.attrib.get(namespaced('normalScreens'), None)
        self.large_screens = tree.attrib.get(namespaced('largeScreens'), None)
        self.xlarge_screens = tree.attrib.get(namespaced('xlargeScreens'), None)
        self.any_density = tree.attrib.get(namespaced('anyDensity'), None)
        self.requires_smallest_width_dp = tree.attrib.get(namespaced('requiresSmallestWidthDp'), None)
        self.compatible_width_limit_dp = tree.attrib.get(namespaced('compatibleWidthLimitDp'), None)
        self.largest_width_limit_dp = tree.attrib.get(namespaced('largestWidthLimitDp'), None)

    def print_diff(self, other, lines: list[str]):
        _compare_and_print(self.resizeable, other.resizeable, 'resizable', lines)
        _compare_and_print(self.small_screens, other.small_screen, 'smallScreens', lines)
        _compare_and_print(self.normal_screens, other.normal_screens, 'normalScreens', lines)
        _compare_and_print(self.large_screens, other.large_screens, 'largeScreens', lines)
        _compare_and_print(self.xlarge_screens, other.xlarge_screens, 'xlargeScreens', lines)
        _compare_and_print(self.any_density, other.any_density, 'anyDensity', lines)
        _compare_and_print(self.requires_smallest_width_dp, other.requires_smallest_width_dp,
                           'requiresSmallestWidthDp', lines)
        _compare_and_print(self.compatible_width_limit_dp, other.compatible_width_limit_dp,
                           'compatibleWidthLimitDp', lines)
        _compare_and_print(self.largest_width_limit_dp, other.largest_width_limit_dp,
                           'largestWidthLimitDp', lines)


@stringify
class CompatibleScreens(object):
    #
    # https://developer.android.com/guide/topics/manifest/manifest-element
    #
    screens = None

    def __init__(self, tree: ElementTree.Element):
        if tree.tag != TAG_COMPATIBLE_SCREENS:
            raise RuntimeError(
                'Expected <{}> as root tag'.format(TAG_COMPATIBLE_SCREENS))

        _set = set()
        for element in tree.findall('screen'):
            size = element.attrib.get(namespaced('screenSize'), None)
            density = element.attrib.get(namespaced('screenDensity'), None)
            _set.add('{}-{}'.format(size, density))

        self.screens = _set

    def print_diff(self, other, lines: list[str]):
        _compare_and_print(self.screens, other.screens, TAG_COMPATIBLE_SCREENS, lines)


@stringify
class UsesSdk(object):
    #
    # https://developer.android.com/guide/topics/manifest/uses-sdk-element
    #
    min_sdk = None
    target_sdk = None
    max_sdk = None

    def __init__(self, tree: ElementTree.Element):
        if tree.tag != TAG_USES_SDK:
            raise RuntimeError(
                'Expected <{}> as root tag'.format(TAG_USES_SDK))
        self.min_sdk = tree.attrib.get(namespaced('minSdkVersion'), None)
        self.target_sdk = tree.attrib.get(namespaced('targetSdkVersion'), None)
        self.max_sdk = tree.attrib.get(namespaced('maxSdkVersion'), None)

    def print_diff(self, other, lines: list[str]):
        _compare_and_print(self.min_sdk, other.min_sdk, 'min sdk', lines)
        _compare_and_print(self.target_sdk, other.target_sdk, 'target sdk', lines)
        _compare_and_print(self.max_sdk, other.max_sdk, 'max sdk', lines)


@stringify
class Manifest(object):
    #
    # https://developer.android.com/guide/topics/manifest/manifest-element
    #
    package = None
    shared_user_id = None
    shared_user_label = None
    version_code = None
    version_name = None
    install_location = None
    application = None
    compatible_screens = None
    permissions = None
    supports_gl_texture = None
    supports_screens = None
    uses_features = None
    uses_permissions = None
    uses_permissions_sdk_23 = None
    uses_sdk = None
    # Optionals for manual check
    has_uses_configuration = False

    def __init__(self, tree: ElementTree.Element):
        if tree.tag != TAG_MANIFEST:
            raise RuntimeError(
                'Expected <{}> as root tag'.format(TAG_MANIFEST))

        self.package = tree.attrib['package']
        self.version_code = tree.attrib.get(namespaced('versionCode'))
        self.version_name = tree.attrib.get(namespaced('versionName'))
        self.shared_user_id = tree.attrib.get(namespaced('sharedUserId'), None)
        self.shared_user_label = tree.attrib.get(namespaced('sharedUserLabel'), None)
        self.install_location = tree.attrib.get(namespaced('installLocation'), None)
        self.permissions = _parse_names_by_tag(tree, TAG_PERMISSION)
        self.uses_features = _parse_names_by_tag(tree, TAG_USES_FEATURE)
        self.uses_permissions = _parse_names_by_tag(tree, TAG_USES_PERMISSION)
        self.uses_permissions_sdk_23 = _parse_names_by_tag(tree, TAG_USES_PERMISSION_SDK_23)
        self.supports_gl_texture = _parse_names_by_tag(tree, TAG_SUPPORTS_GL_TEXTURE)
        self.application = Application(tree.find(TAG_APPLICATION))

        uses_sdk_tree = tree.find(TAG_USES_SDK)
        if uses_sdk_tree is None:
            self.uses_sdk = None
        else:
            self.uses_sdk = UsesSdk(uses_sdk_tree)

        supports_screens_tree = tree.find(TAG_SUPPORTS_SCREENS)
        if supports_screens_tree is None:
            self.supports_screens = None
        else:
            self.supports_screens = SupportsScreens(supports_screens_tree)

        compatible_screens_tree = tree.find(TAG_COMPATIBLE_SCREENS)
        if compatible_screens_tree is None:
            self.compatible_screens = None
        else:
            self.compatible_screens = CompatibleScreens(compatible_screens_tree)

        self.has_uses_configuration = tree.find(TAG_USES_CONFIGURATION) is not None

    def print_diff(self, other):
        lines = []
        manual_checks = []
        _compare_and_print(self.package, other.package, 'package', lines)
        _compare_and_print(self.shared_user_id, other.shared_user_id, 'sharedUserId', lines)
        _compare_and_print(self.shared_user_label, other.shared_user_label, 'sharedUserLabel', lines)
        _compare_and_print(self.version_code, other.version_code, 'versionCode', lines)
        _compare_and_print(self.version_name, other.version_name, 'versionName', lines)
        _compare_and_print(self.install_location, other.install_location, 'installLocation', lines)
        _compare_and_print(self.permissions, other.permissions, TAG_PERMISSION, lines)
        _compare_and_print(self.uses_features, other.uses_features, TAG_USES_FEATURE, lines)
        _compare_and_print(self.uses_permissions, other.uses_permissions, TAG_USES_PERMISSION, lines)
        _compare_and_print(self.uses_permissions_sdk_23, other.uses_permissions_sdk_23, TAG_USES_PERMISSION_SDK_23,
                           lines)
        _compare_and_print(self.supports_gl_texture, other.supports_gl_texture, TAG_SUPPORTS_GL_TEXTURE, lines)

        if self.uses_sdk is not None and other.uses_sdk is not None:
            self.uses_sdk.print_diff(other.uses_sdk, lines)
        elif (self.uses_sdk is not None) != (other.uses_sdk is not None):
            manual_checks.append(TAG_USES_SDK)

        if self.has_uses_configuration is None or other.uses_sdk is None:
            manual_checks.append(TAG_USES_CONFIGURATION)

        if self.compatible_screens is not None and other.compatible_screens is not None:
            self.compatible_screens.print_diff(other.compatible_screens, lines)
        elif (self.compatible_screens is None) != (other.compatible_screens is None):
            manual_checks.append(TAG_COMPATIBLE_SCREENS)

        if self.supports_screens is not None and other.supports_screens is not None:
            self.supports_screens.print_diff(other.supports_screens, lines)
        elif (self.supports_screens is None) != (other.supports_screens is None):
            manual_checks.append(TAG_SUPPORTS_SCREENS)

        self.application.print_diff(other.application, lines)

        if len(manual_checks) > 0:
            lines.append('Manually check these sections:')
            for manual_check in manual_checks:
                lines.append('    {}'.format(manual_check))
        return '\n'.join(lines)


def compare_manifests(prev_manifest: str, current_manifest: str) -> str:
    if not prev_manifest and not current_manifest:
        return 'Cannot get manifests'
    if not prev_manifest:
        return 'Cannot get previous version\'s manifest'
    if not current_manifest:
        return 'Cannot get current version\'s manifest'

    lhs_tree = ElementTree.ElementTree(ElementTree.fromstring(prev_manifest))
    lhs_manifest = Manifest(lhs_tree.getroot())
    rhs_tree = ElementTree.ElementTree(
        ElementTree.fromstring(current_manifest))
    rhs_manifest = Manifest(rhs_tree.getroot())
    return lhs_manifest.print_diff(rhs_manifest)
