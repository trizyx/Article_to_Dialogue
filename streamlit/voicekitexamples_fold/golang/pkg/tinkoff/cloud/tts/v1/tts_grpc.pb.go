// Code generated by protoc-gen-go-grpc. DO NOT EDIT.
// versions:
// - protoc-gen-go-grpc v1.2.0
// - protoc             v3.19.4
// source: tinkoff/cloud/tts/v1/tts.proto

package v1

import (
	context "context"
	grpc "google.golang.org/grpc"
	codes "google.golang.org/grpc/codes"
	status "google.golang.org/grpc/status"
)

// This is a compile-time assertion to ensure that this generated file
// is compatible with the grpc package it is being compiled against.
// Requires gRPC-Go v1.32.0 or later.
const _ = grpc.SupportPackageIsVersion7

// TextToSpeechClient is the client API for TextToSpeech service.
//
// For semantics around ctx use and closing/ending streaming RPCs, please refer to https://pkg.go.dev/google.golang.org/grpc/?tab=doc#ClientConn.NewStream.
type TextToSpeechClient interface {
	ListVoices(ctx context.Context, in *ListVoicesRequest, opts ...grpc.CallOption) (*ListVoicesResponses, error)
	Synthesize(ctx context.Context, in *SynthesizeSpeechRequest, opts ...grpc.CallOption) (*SynthesizeSpeechResponse, error)
	StreamingSynthesize(ctx context.Context, in *SynthesizeSpeechRequest, opts ...grpc.CallOption) (TextToSpeech_StreamingSynthesizeClient, error)
}

type textToSpeechClient struct {
	cc grpc.ClientConnInterface
}

func NewTextToSpeechClient(cc grpc.ClientConnInterface) TextToSpeechClient {
	return &textToSpeechClient{cc}
}

func (c *textToSpeechClient) ListVoices(ctx context.Context, in *ListVoicesRequest, opts ...grpc.CallOption) (*ListVoicesResponses, error) {
	out := new(ListVoicesResponses)
	err := c.cc.Invoke(ctx, "/tinkoff.cloud.tts.v1.TextToSpeech/ListVoices", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *textToSpeechClient) Synthesize(ctx context.Context, in *SynthesizeSpeechRequest, opts ...grpc.CallOption) (*SynthesizeSpeechResponse, error) {
	out := new(SynthesizeSpeechResponse)
	err := c.cc.Invoke(ctx, "/tinkoff.cloud.tts.v1.TextToSpeech/Synthesize", in, out, opts...)
	if err != nil {
		return nil, err
	}
	return out, nil
}

func (c *textToSpeechClient) StreamingSynthesize(ctx context.Context, in *SynthesizeSpeechRequest, opts ...grpc.CallOption) (TextToSpeech_StreamingSynthesizeClient, error) {
	stream, err := c.cc.NewStream(ctx, &TextToSpeech_ServiceDesc.Streams[0], "/tinkoff.cloud.tts.v1.TextToSpeech/StreamingSynthesize", opts...)
	if err != nil {
		return nil, err
	}
	x := &textToSpeechStreamingSynthesizeClient{stream}
	if err := x.ClientStream.SendMsg(in); err != nil {
		return nil, err
	}
	if err := x.ClientStream.CloseSend(); err != nil {
		return nil, err
	}
	return x, nil
}

type TextToSpeech_StreamingSynthesizeClient interface {
	Recv() (*StreamingSynthesizeSpeechResponse, error)
	grpc.ClientStream
}

type textToSpeechStreamingSynthesizeClient struct {
	grpc.ClientStream
}

func (x *textToSpeechStreamingSynthesizeClient) Recv() (*StreamingSynthesizeSpeechResponse, error) {
	m := new(StreamingSynthesizeSpeechResponse)
	if err := x.ClientStream.RecvMsg(m); err != nil {
		return nil, err
	}
	return m, nil
}

// TextToSpeechServer is the server API for TextToSpeech service.
// All implementations must embed UnimplementedTextToSpeechServer
// for forward compatibility
type TextToSpeechServer interface {
	ListVoices(context.Context, *ListVoicesRequest) (*ListVoicesResponses, error)
	Synthesize(context.Context, *SynthesizeSpeechRequest) (*SynthesizeSpeechResponse, error)
	StreamingSynthesize(*SynthesizeSpeechRequest, TextToSpeech_StreamingSynthesizeServer) error
	mustEmbedUnimplementedTextToSpeechServer()
}

// UnimplementedTextToSpeechServer must be embedded to have forward compatible implementations.
type UnimplementedTextToSpeechServer struct {
}

func (UnimplementedTextToSpeechServer) ListVoices(context.Context, *ListVoicesRequest) (*ListVoicesResponses, error) {
	return nil, status.Errorf(codes.Unimplemented, "method ListVoices not implemented")
}
func (UnimplementedTextToSpeechServer) Synthesize(context.Context, *SynthesizeSpeechRequest) (*SynthesizeSpeechResponse, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Synthesize not implemented")
}
func (UnimplementedTextToSpeechServer) StreamingSynthesize(*SynthesizeSpeechRequest, TextToSpeech_StreamingSynthesizeServer) error {
	return status.Errorf(codes.Unimplemented, "method StreamingSynthesize not implemented")
}
func (UnimplementedTextToSpeechServer) mustEmbedUnimplementedTextToSpeechServer() {}

// UnsafeTextToSpeechServer may be embedded to opt out of forward compatibility for this service.
// Use of this interface is not recommended, as added methods to TextToSpeechServer will
// result in compilation errors.
type UnsafeTextToSpeechServer interface {
	mustEmbedUnimplementedTextToSpeechServer()
}

func RegisterTextToSpeechServer(s grpc.ServiceRegistrar, srv TextToSpeechServer) {
	s.RegisterService(&TextToSpeech_ServiceDesc, srv)
}

func _TextToSpeech_ListVoices_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(ListVoicesRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(TextToSpeechServer).ListVoices(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/tinkoff.cloud.tts.v1.TextToSpeech/ListVoices",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(TextToSpeechServer).ListVoices(ctx, req.(*ListVoicesRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _TextToSpeech_Synthesize_Handler(srv interface{}, ctx context.Context, dec func(interface{}) error, interceptor grpc.UnaryServerInterceptor) (interface{}, error) {
	in := new(SynthesizeSpeechRequest)
	if err := dec(in); err != nil {
		return nil, err
	}
	if interceptor == nil {
		return srv.(TextToSpeechServer).Synthesize(ctx, in)
	}
	info := &grpc.UnaryServerInfo{
		Server:     srv,
		FullMethod: "/tinkoff.cloud.tts.v1.TextToSpeech/Synthesize",
	}
	handler := func(ctx context.Context, req interface{}) (interface{}, error) {
		return srv.(TextToSpeechServer).Synthesize(ctx, req.(*SynthesizeSpeechRequest))
	}
	return interceptor(ctx, in, info, handler)
}

func _TextToSpeech_StreamingSynthesize_Handler(srv interface{}, stream grpc.ServerStream) error {
	m := new(SynthesizeSpeechRequest)
	if err := stream.RecvMsg(m); err != nil {
		return err
	}
	return srv.(TextToSpeechServer).StreamingSynthesize(m, &textToSpeechStreamingSynthesizeServer{stream})
}

type TextToSpeech_StreamingSynthesizeServer interface {
	Send(*StreamingSynthesizeSpeechResponse) error
	grpc.ServerStream
}

type textToSpeechStreamingSynthesizeServer struct {
	grpc.ServerStream
}

func (x *textToSpeechStreamingSynthesizeServer) Send(m *StreamingSynthesizeSpeechResponse) error {
	return x.ServerStream.SendMsg(m)
}

// TextToSpeech_ServiceDesc is the grpc.ServiceDesc for TextToSpeech service.
// It's only intended for direct use with grpc.RegisterService,
// and not to be introspected or modified (even as a copy)
var TextToSpeech_ServiceDesc = grpc.ServiceDesc{
	ServiceName: "tinkoff.cloud.tts.v1.TextToSpeech",
	HandlerType: (*TextToSpeechServer)(nil),
	Methods: []grpc.MethodDesc{
		{
			MethodName: "ListVoices",
			Handler:    _TextToSpeech_ListVoices_Handler,
		},
		{
			MethodName: "Synthesize",
			Handler:    _TextToSpeech_Synthesize_Handler,
		},
	},
	Streams: []grpc.StreamDesc{
		{
			StreamName:    "StreamingSynthesize",
			Handler:       _TextToSpeech_StreamingSynthesize_Handler,
			ServerStreams: true,
		},
	},
	Metadata: "tinkoff/cloud/tts/v1/tts.proto",
}
