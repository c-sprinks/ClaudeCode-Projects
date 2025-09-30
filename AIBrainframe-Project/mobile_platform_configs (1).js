// metro.config.js - Metro bundler configuration
const {getDefaultConfig, mergeConfig} = require('@react-native/metro-config');

const config = {
  resolver: {
    assetExts: ['bin', 'txt', 'jpg', 'png', 'json', 'gif', 'webp', 'svg'],
  },
};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);

// babel.config.js - Babel configuration
module.exports = {
  presets: ['module:metro-react-native-babel-preset'],
  plugins: [
    'react-native-reanimated/plugin',
  ],
};

// react-native.config.js - React Native CLI configuration
module.exports = {
  dependencies: {
    'react-native-vector-icons': {
      platforms: {
        ios: {
          xcodeprojPath: 'ios/AIBrainFrameMobile.xcodeproj',
          plistPath: 'ios/AIBrainFrameMobile/Info.plist',
        },
      },
    },
  },
  assets: ['./assets/fonts/'],
};

// ios/Podfile - iOS CocoaPods configuration
platform :ios, '12.4'
require_relative '../node_modules/react-native/scripts/react_