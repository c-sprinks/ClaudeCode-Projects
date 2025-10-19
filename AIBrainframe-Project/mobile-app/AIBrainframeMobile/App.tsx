// App.tsx - AIBrainFrame Complete Mobile Application
import React, {useState, useEffect, useRef, useCallback} from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  StyleSheet,
  SafeAreaView,
  KeyboardAvoidingView,
  Platform,
  Alert,
  Animated,
  StatusBar,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import LinearGradient from 'react-native-linear-gradient';
import Icon from 'react-native-vector-icons/MaterialIcons';

// const {width, height} = Dimensions.get('window');
const API_BASE = 'http://108.254.44.67:8000';  // Production LBOB server

// Type definitions
interface Message {
  message_id?: number;
  conversation_id: number;
  sender_type: string;
  message_text: string;
  timestamp: string;
  is_solution?: boolean;
}

interface Conversation {
  conversation_id: number;
  title: string;
  status: string;
  started_at: string;
}

// LBOB Character Component
const LBOBCharacter: React.FC<{isTyping?: boolean; size?: number}> = ({
  isTyping,
  size = 40,
}) => {
  const pulseAnim = useRef(new Animated.Value(1)).current;
  const bounceAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    // Pulse animation
    const pulseLoop = Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.2,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
      ]),
    );

    // Bounce animation when typing
    const bounceLoop = Animated.loop(
      Animated.sequence([
        Animated.timing(bounceAnim, {
          toValue: 1,
          duration: 500,
          useNativeDriver: true,
        }),
        Animated.timing(bounceAnim, {
          toValue: 0,
          duration: 500,
          useNativeDriver: true,
        }),
      ]),
    );

    pulseLoop.start();
    if (isTyping) {
      bounceLoop.start();
    } else {
      bounceLoop.stop();
      bounceAnim.setValue(0);
    }

    return () => {
      pulseLoop.stop();
      bounceLoop.stop();
    };
  }, [isTyping, pulseAnim, bounceAnim]);

  const bounceTransform = {
    transform: [
      {
        translateY: bounceAnim.interpolate({
          inputRange: [0, 1],
          outputRange: [0, -5],
        }),
      },
    ],
  };

  return (
    <Animated.View
      style={[
        styles.lbobContainer,
        {
          width: size,
          height: size,
          transform: [{scale: pulseAnim}],
        },
      ]}>
      <LinearGradient
        colors={['#667eea', '#764ba2']}
        style={[styles.lbobCharacter, {width: size, height: size}]}>
        <Animated.Text style={[styles.lbobEmoji, bounceTransform]}>
          🤖
        </Animated.Text>
      </LinearGradient>
    </Animated.View>
  );
};

// API Service
const apiService = {
  request: async (endpoint: string, options: any = {}) => {
    const token = await AsyncStorage.getItem('token');
    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(token && {Authorization: `Bearer ${token}`}),
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  },

  login: async (username: string, password: string) => {
    const response = await fetch(`${API_BASE}/users/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({username, password}),
    });

    if (!response.ok) {
      throw new Error('Invalid credentials');
    }
    const data = await response.json();
    await AsyncStorage.setItem('token', data.access_token);
    return data;
  },

  getConversations: () => apiService.request('/conversations/'),
  createConversation: (title: string) =>
    apiService.request('/conversations/', {
      method: 'POST',
      body: JSON.stringify({title}),
    }),
  getMessages: (conversationId: number) =>
    apiService.request(`/conversations/${conversationId}/messages`),
  sendMessage: (conversationId: number, message: string) =>
    apiService.request(`/conversations/${conversationId}/messages`, {
      method: 'POST',
      body: JSON.stringify({message_text: message}),
    }),
};

// Login Screen
const LoginScreen: React.FC<{onLogin: () => void}> = ({onLogin}) => {
  const [username, setUsername] = useState('testtech');
  const [password, setPassword] = useState('password123');
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Error', 'Please enter username and password');
      return;
    }

    setLoading(true);
    try {
      await apiService.login(username, password);
      onLogin();
    } catch (error) {
      Alert.alert('Login Failed', 'Invalid username or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <LinearGradient
      colors={['#667eea', '#764ba2']}
      style={styles.loginContainer}>
      <StatusBar barStyle="light-content" />
      <View style={styles.loginCard}>
        <View style={styles.logoContainer}>
          <LBOBCharacter size={80} />
          <Text style={styles.logoText}>AIBrainFrame</Text>
          <Text style={styles.logoSubtext}>LBOB AI Assistant</Text>
        </View>

        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Username"
            value={username}
            onChangeText={setUsername}
            autoCapitalize="none"
          />
          <TextInput
            style={styles.input}
            placeholder="Password"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />
        </View>

        <TouchableOpacity
          style={[styles.loginButton, loading && styles.loginButtonDisabled]}
          onPress={handleLogin}
          disabled={loading}>
          <LinearGradient
            colors={['#667eea', '#764ba2']}
            style={styles.loginButtonGradient}>
            <Text style={styles.loginButtonText}>
              {loading ? 'Logging in...' : 'Login'}
            </Text>
          </LinearGradient>
        </TouchableOpacity>
      </View>
    </LinearGradient>
  );
};

// Message Component
const MessageItem: React.FC<{message: Message; isTyping?: boolean}> = ({
  message,
  isTyping,
}) => {
  const isUser = message.sender_type === 'user';

  return (
    <View
      style={[styles.messageContainer, isUser && styles.userMessageContainer]}>
      {!isUser && (
        <View style={styles.avatarContainer}>
          <LBOBCharacter isTyping={isTyping} size={32} />
        </View>
      )}

      <View style={[styles.messageBubble, isUser && styles.userMessageBubble]}>
        {isTyping ? (
          <View style={styles.typingContainer}>
            <Text style={styles.typingText}>LBOB is thinking</Text>
            <View style={styles.typingDotsContainer}>
              <View style={styles.typingDot} />
              <View style={styles.typingDot} />
              <View style={styles.typingDot} />
            </View>
          </View>
        ) : (
          <Text style={[styles.messageText, isUser && styles.userMessageText]}>
            {message.message_text}
          </Text>
        )}
      </View>

      {isUser && (
        <View style={styles.userAvatarContainer}>
          <LinearGradient
            colors={['#4CAF50', '#45a049']}
            style={styles.userAvatar}>
            <Icon name="person" size={20} color="white" />
          </LinearGradient>
        </View>
      )}
    </View>
  );
};

// Chat Screen
const ChatScreen: React.FC<{
  conversation: Conversation;
  onBack: () => void;
}> = ({conversation, onBack}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const flatListRef = useRef<FlatList>(null);

  const loadMessages = useCallback(async () => {
    try {
      const data = await apiService.getMessages(conversation.conversation_id);
      setMessages(data);
    } catch (error) {
      Alert.alert('Error', 'Failed to load messages');
    }
  }, [conversation.conversation_id]);

  useEffect(() => {
    loadMessages();
  }, [conversation, loadMessages]);

  const sendMessage = async () => {
    if (!inputText.trim() || loading) {
      return;
    }

    const userMessage: Message = {
      sender_type: 'user',
      message_text: inputText,
      timestamp: new Date().toISOString(),
      conversation_id: conversation.conversation_id,
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setLoading(true);
    setIsTyping(true);

    try {
      const response = await apiService.sendMessage(
        conversation.conversation_id,
        inputText,
      );
      setIsTyping(false);
      setMessages(prev => [...prev, response]);
    } catch (error) {
      setIsTyping(false);
      Alert.alert('Error', 'Failed to send message');
    } finally {
      setLoading(false);
    }
  };

  const renderMessage = ({item}: {item: Message}) => (
    <MessageItem message={item} isTyping={false} />
  );

  return (
    <SafeAreaView style={styles.chatContainer}>
      <StatusBar barStyle="dark-content" />

      {/* Header */}
      <View style={styles.chatHeader}>
        <TouchableOpacity onPress={onBack} style={styles.backButton}>
          <Icon name="arrow-back" size={24} color="#333" />
        </TouchableOpacity>
        <View style={styles.chatHeaderContent}>
          <Text style={styles.chatTitle}>{conversation.title}</Text>
          <Text style={styles.chatSubtitle}>Chat with LBOB</Text>
        </View>
        <LBOBCharacter size={32} />
      </View>

      {/* Messages */}
      <FlatList
        ref={flatListRef}
        data={messages}
        renderItem={renderMessage}
        keyExtractor={(item, index) => index.toString()}
        style={styles.messagesList}
        contentContainerStyle={styles.messagesContent}
        onContentSizeChange={() => flatListRef.current?.scrollToEnd()}
        onLayout={() => flatListRef.current?.scrollToEnd()}
      />

      {/* Typing Indicator */}
      {isTyping && (
        <MessageItem
          message={{
            sender_type: 'ai',
            message_text: '',
            conversation_id: conversation.conversation_id,
            timestamp: '',
          }}
          isTyping={true}
        />
      )}

      {/* Input */}
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.inputSection}>
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.messageInput}
            placeholder="Describe your technical issue..."
            value={inputText}
            onChangeText={setInputText}
            multiline
            maxLength={1000}
          />
          <TouchableOpacity
            style={[
              styles.sendButton,
              (!inputText.trim() || loading) && styles.sendButtonDisabled,
            ]}
            onPress={sendMessage}
            disabled={!inputText.trim() || loading}>
            <LinearGradient
              colors={['#667eea', '#764ba2']}
              style={styles.sendButtonGradient}>
              <Icon name="send" size={20} color="white" />
            </LinearGradient>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

// Conversations List Screen
const ConversationsScreen: React.FC<{
  onSelectConversation: (conversation: Conversation) => void;
  onNewConversation: (conversation: Conversation) => void;
}> = ({onSelectConversation, onNewConversation: _onNewConversation}) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    try {
      const data = await apiService.getConversations();
      setConversations(data);
    } catch (error) {
      Alert.alert('Error', 'Failed to load conversations');
    } finally {
      setLoading(false);
    }
  };

  const createNewConversation = async () => {
    try {
      const conversation = await apiService.createConversation(
        'New Troubleshooting Session',
      );
      setConversations(prev => [conversation, ...prev]);
      onSelectConversation(conversation);
    } catch (error) {
      Alert.alert('Error', 'Failed to create conversation');
    }
  };

  const renderConversation = ({item}: {item: Conversation}) => (
    <TouchableOpacity
      style={styles.conversationItem}
      onPress={() => onSelectConversation(item)}>
      <View style={styles.conversationContent}>
        <Text style={styles.conversationTitle}>{item.title}</Text>
        <Text style={styles.conversationDate}>
          {new Date(item.started_at).toLocaleDateString()}
        </Text>
      </View>
      <Icon name="chevron-right" size={24} color="#ccc" />
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.conversationsContainer}>
      <StatusBar barStyle="dark-content" />

      <View style={styles.conversationsHeader}>
        <View style={styles.headerTitleContainer}>
          <LBOBCharacter size={40} />
          <View style={styles.headerTextContainer}>
            <Text style={styles.headerTitle}>AIBrainFrame</Text>
            <Text style={styles.headerSubtitle}>Your AI Assistant</Text>
          </View>
        </View>
      </View>

      <TouchableOpacity
        style={styles.newConversationButton}
        onPress={createNewConversation}>
        <LinearGradient
          colors={['#667eea', '#764ba2']}
          style={styles.newConversationGradient}>
          <Icon name="add" size={24} color="white" />
          <Text style={styles.newConversationText}>New Conversation</Text>
        </LinearGradient>
      </TouchableOpacity>

      <FlatList
        data={conversations}
        renderItem={renderConversation}
        keyExtractor={item => item.conversation_id.toString()}
        style={styles.conversationsList}
        refreshing={loading}
        onRefresh={loadConversations}
      />
    </SafeAreaView>
  );
};

// Main App Component
const App: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentScreen, setCurrentScreen] = useState('conversations');
  const [selectedConversation, setSelectedConversation] =
    useState<Conversation | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = await AsyncStorage.getItem('token');
      setIsAuthenticated(!!token);
    } catch (error) {
      console.error('Auth check failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = () => {
    setIsAuthenticated(true);
    setCurrentScreen('conversations');
  };

  // const handleLogout = async () => {
  //   await AsyncStorage.removeItem('token');
  //   setIsAuthenticated(false);
  //   setCurrentScreen('conversations');
  //   setSelectedConversation(null);
  // };

  const handleSelectConversation = (conversation: Conversation) => {
    setSelectedConversation(conversation);
    setCurrentScreen('chat');
  };

  const handleBackToConversations = () => {
    setCurrentScreen('conversations');
    setSelectedConversation(null);
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <LBOBCharacter size={60} isTyping={true} />
        <Text style={styles.loadingText}>Loading...</Text>
      </View>
    );
  }

  if (!isAuthenticated) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  if (currentScreen === 'chat' && selectedConversation) {
    return (
      <ChatScreen
        conversation={selectedConversation}
        onBack={handleBackToConversations}
      />
    );
  }

  return (
    <ConversationsScreen
      onSelectConversation={handleSelectConversation}
      onNewConversation={handleSelectConversation}
    />
  );
};

// Comprehensive Styles
const styles = StyleSheet.create({
  // Login Styles
  loginContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  loginCard: {
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 30,
    width: '100%',
    maxWidth: 400,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 10},
    shadowOpacity: 0.3,
    shadowRadius: 20,
    elevation: 10,
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: 30,
  },
  logoText: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 10,
  },
  logoSubtext: {
    fontSize: 16,
    color: '#666',
    marginTop: 5,
  },
  inputContainer: {
    marginBottom: 20,
  },
  input: {
    borderWidth: 2,
    borderColor: '#e0e0e0',
    borderRadius: 12,
    padding: 15,
    fontSize: 16,
    marginBottom: 15,
    backgroundColor: '#f8f8f8',
  },
  loginButton: {
    borderRadius: 12,
    overflow: 'hidden',
  },
  loginButtonGradient: {
    padding: 15,
    alignItems: 'center',
  },
  loginButtonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  loginButtonDisabled: {
    opacity: 0.6,
  },

  // LBOB Character Styles
  lbobContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  lbobCharacter: {
    borderRadius: 50,
    alignItems: 'center',
    justifyContent: 'center',
  },
  lbobEmoji: {
    fontSize: 20,
  },

  // Conversations Screen Styles
  conversationsContainer: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  conversationsHeader: {
    backgroundColor: 'white',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  headerTitleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerTextContainer: {
    marginLeft: 15,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
  },
  headerSubtitle: {
    fontSize: 16,
    color: '#666',
  },
  newConversationButton: {
    margin: 20,
    borderRadius: 12,
    overflow: 'hidden',
  },
  newConversationGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 15,
  },
  newConversationText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 10,
  },
  conversationsList: {
    flex: 1,
  },
  conversationItem: {
    backgroundColor: 'white',
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
    marginHorizontal: 20,
    marginBottom: 10,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  conversationContent: {
    flex: 1,
  },
  conversationTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  conversationDate: {
    fontSize: 14,
    color: '#666',
  },

  // Chat Screen Styles
  chatContainer: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  chatHeader: {
    backgroundColor: 'white',
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  backButton: {
    marginRight: 15,
  },
  chatHeaderContent: {
    flex: 1,
  },
  chatTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  chatSubtitle: {
    fontSize: 14,
    color: '#666',
  },
  messagesList: {
    flex: 1,
  },
  messagesContent: {
    padding: 20,
  },
  messageContainer: {
    flexDirection: 'row',
    marginBottom: 15,
    alignItems: 'flex-end',
  },
  userMessageContainer: {
    flexDirection: 'row-reverse',
  },
  avatarContainer: {
    marginRight: 10,
  },
  userAvatarContainer: {
    marginLeft: 10,
  },
  userAvatar: {
    width: 32,
    height: 32,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
  },
  messageBubble: {
    backgroundColor: 'white',
    padding: 15,
    borderRadius: 20,
    maxWidth: '70%',
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 1},
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  userMessageBubble: {
    backgroundColor: '#667eea',
  },
  messageText: {
    fontSize: 16,
    lineHeight: 22,
    color: '#333',
  },
  userMessageText: {
    color: 'white',
  },
  typingContainer: {
    alignItems: 'center',
  },
  typingText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
  },
  typingDotsContainer: {
    flexDirection: 'row',
  },
  typingDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: '#667eea',
    marginHorizontal: 2,
  },
  inputSection: {
    backgroundColor: 'white',
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  messageInput: {
    flex: 1,
    borderWidth: 2,
    borderColor: '#e0e0e0',
    borderRadius: 25,
    paddingHorizontal: 20,
    paddingVertical: 10,
    fontSize: 16,
    maxHeight: 100,
    marginRight: 10,
    backgroundColor: '#f8f8f8',
  },
  sendButton: {
    borderRadius: 25,
    overflow: 'hidden',
  },
  sendButtonGradient: {
    width: 50,
    height: 50,
    alignItems: 'center',
    justifyContent: 'center',
  },
  sendButtonDisabled: {
    opacity: 0.6,
  },

  // Loading Styles
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  loadingText: {
    fontSize: 18,
    color: '#666',
    marginTop: 20,
  },
});

export default App;
