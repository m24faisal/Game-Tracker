// Copyright 2020-2023 Bloomberg Finance L.P.
// SPDX-License-Identifier: Apache-2.0
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <rmqamqpt_connectionmethod.h>

#include <rmqamqpt_connectionclose.h>
#include <rmqamqpt_connectioncloseok.h>
#include <rmqamqpt_connectionopen.h>
#include <rmqamqpt_connectionopenok.h>
#include <rmqamqpt_connectionstart.h>
#include <rmqamqpt_connectionstartok.h>
#include <rmqamqpt_connectiontune.h>
#include <rmqamqpt_connectiontuneok.h>
#include <rmqamqpt_types.h>

#include <ball_log.h>

#include <bsl_cstddef.h>

namespace BloombergLP {
namespace rmqamqpt {
namespace {
BALL_LOG_SET_NAMESPACE_CATEGORY("RMQAMQPT.CONNECTIONMETHOD")

template <typename T>
bool decodeMethod(ConnectionMethod* connMethod,
                  const uint8_t* data,
                  bsl::size_t dataLen)
{
    connMethod->createInPlace<T>();
    return T::decode(&connMethod->the<T>(), data, dataLen);
}

#define DECODE_METHOD(method)                                                  \
    case method::METHOD_ID:                                                    \
        return decodeMethod<method>(connMethod, data, dataLen);

bool decodeConnectionMethodPayload(ConnectionMethod* connMethod,
                                   uint16_t methodId,
                                   const uint8_t* data,
                                   bsl::size_t dataLen)
{
    switch (methodId) {
        DECODE_METHOD(ConnectionStart)
        DECODE_METHOD(ConnectionStartOk)
        DECODE_METHOD(ConnectionTune)
        DECODE_METHOD(ConnectionTuneOk)
        DECODE_METHOD(ConnectionOpen)
        DECODE_METHOD(ConnectionOpenOk)
        DECODE_METHOD(ConnectionClose)
        DECODE_METHOD(ConnectionCloseOk)
        default: {
            BALL_LOG_ERROR
                << "Failed to decode ConnectionMethod with unknown id: "
                << methodId;

            return false;
        }
    }
}

#undef DECODE_METHOD

struct ConnectionMethodEncoder {

    ConnectionMethodEncoder(Writer& os)
    : d_os(os)
    {
    }

    template <typename T>
    void operator()(const T& method) const
    {
        Types::write(d_os, bdlb::BigEndianUint16::make(T::METHOD_ID));
        T::encode(d_os, method);
    }

    void operator()(const bslmf::Nil&) const {}

  private:
    Writer& d_os;
};
struct MethodIdFetcher {
    typedef rmqamqpt::Constants::AMQPMethodId ResultType;

    template <typename T>
    ResultType operator()(const T&) const
    {
        return T::METHOD_ID;
    }

    ResultType operator()(const bslmf::Nil&) const
    {
        return rmqamqpt::Constants::NO_METHOD;
    }
};

struct MethodSizeFetcher {
    typedef size_t ResultType;

    template <typename T>
    ResultType operator()(const T& methodSpec) const
    {
        return methodSpec.encodedSize();
    }

    ResultType operator()(const bslmf::Nil&) const { return 0; }
};

} // namespace

rmqamqpt::Constants::AMQPMethodId ConnectionMethod::methodId() const
{
    return this->apply(MethodIdFetcher());
}

size_t ConnectionMethod::encodedSize() const
{
    return sizeof(uint16_t) + this->apply(MethodSizeFetcher());
}

bool ConnectionMethod::Util::decode(ConnectionMethod* connMethod,
                                    const uint8_t* data,
                                    bsl::size_t dataLength)
{
    bdlb::BigEndianUint16 methodId;

    if (dataLength < sizeof(methodId)) {

        BALL_LOG_ERROR << "Not enough data to read methodId";
        return false;
    }

    memcpy(&methodId, data, sizeof(methodId));

    return decodeConnectionMethodPayload(connMethod,
                                         methodId,
                                         data + sizeof(methodId),
                                         dataLength - sizeof(methodId));
}

void ConnectionMethod::Util::encode(Writer& output,
                                    const ConnectionMethod& connMethod)
{
    connMethod.apply(ConnectionMethodEncoder(output));
}

ConnectionMethod::ConnectionMethod() {}

} // namespace rmqamqpt
} // namespace BloombergLP
